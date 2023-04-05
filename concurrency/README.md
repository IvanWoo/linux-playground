# concurrency

## stack size

```sh
gcc stack-prob.c && ./a.out
```

around `8192 KB` == `8 MB`

## challenges of multi-core execution

### no atomicity

多个线程同时执行 sum++。我们可以使用 inline assembly 要求把求和翻译成一条指令，
但除非引入额外的硬件机制，依然无法保证单条指令在多处理器上执行的原子性。

classical transaction problem

```sh
$ gcc alipay.c && ./a.out
balance = 18446744073709551516
```

### no sequence

compilers make it harder!

```sh
gcc sum.c && ./a.out
```

optimization O2 will make the program right and O1 will have consistent wrong answer

```sh
$ gcc sum.c -O2 && ./a.out
sum = 200000000
```

```sh
$ gcc sum.c -O1 && ./a.out
sum = 100000000
```

check the assembly code to figure out why

```sh
gcc sum.c -O1 -c
objdump -d sum.o > 01.txt
```

### no visibility between cpus

### take away

- 指令/代码执行原子性假设不再成立
- 程序的顺序执行假设不再成立
- 多处理器间内存访问无法即时可见

## peterson algorithm (no lock)

```sh
gcc peterson.c && ./a.out
```

## locks

### spinlock(自旋锁)

```sh
gcc sum-spinlock.c && ./a.out
```

### Scalability: 性能的新维度

同一份计算任务，时间 (CPU cycles) 和空间 (mapped memory) 会随处理器数量的增长而变化。

```sh
gcc sum-scalability.c
```

```sh
root@ubuntu:/vagrant/concurrency# time ./a.out 1

real    0m0.140s
user    0m0.121s
sys     0m0.004s
root@ubuntu:/vagrant/concurrency# time ./a.out 2

real    0m0.610s
user    0m1.184s
sys     0m0.000s
root@ubuntu:/vagrant/concurrency# time ./a.out 4

real    0m0.881s
user    0m1.717s
sys     0m0.001s
root@ubuntu:/vagrant/concurrency# time ./a.out 8

real    0m1.217s
user    0m2.322s
sys     0m0.000s
root@ubuntu:/vagrant/concurrency# time ./a.out 16

real    0m2.774s
user    0m5.429s
sys     0m0.000s
```

### analyze

自旋锁 (线程直接共享 locked)

- 更快的 fast path
  - xchg 成功 → 立即进入临界区，开销很小
- 更慢的 slow path
  - xchg 失败 → 浪费 CPU 自旋等待

互斥锁 (通过系统调用访问 locked)

- 更经济的 slow path
  - 上锁失败线程不再占用 CPU
- 更慢的 fast path
  - 即便上锁成功也需要进出内核 (syscall)

### gdb debug

```sh
gcc -g sum-mutex.c
gdb a.out
```

```sh
break main
break 10
run
print sum
backtrace
step
next
continue
quit
```

## synchronization

### producers and consumers

```sh
gcc pc-mutex.c && ./a.out 3
```

test the results

```sh
./a.out 30 | python3 pc-check.py 30
```

### conditional variables

条件变量：理想与实现之间的折衷
一把互斥锁 + 一个 “条件变量” + 手工唤醒

- wait(cv, mutex) 💤
  - 调用时必须保证已经获得 mutex
  - wait 释放 mutex、进入睡眠状态(no spin check)
  - 被唤醒后需要重新执行 lock(mutex)
- signal/notify(cv) 💬
  - 随机私信一个等待者：醒醒
  - 如果有线程正在等待 cv，则唤醒其中一个线程
- broadcast/notifyAll(cv) 📣
  - 叫醒所有人
  - 唤醒全部正在等待 cv 的线程

wrong implementation

only trigger the wrong states when more than 1 consumers and producers

```sh
gcc pc-cv.c && ./a.out 1 3
```

right with while

```sh
gcc pc-cv-while.c && ./a.out 1 3
```

more complicated case

```sh
gcc fish.c && ./a.out
```

万能并行计算框架

```c
struct work {
  void (*run)(void *arg);
  void *arg;
}

void Tworker() {
  while (1) {
    struct work *work;
    wait_until(has_new_work() || all_done) {
      work = get_work();
    }
    if (!work) break;
    else {
      work->run(work->arg); // 允许生成新的 work (注意互斥)
      release(work);  // 注意回收 work 分配的资源
    }
  }
}
```

用 wait + broadcast 实现 `WAIT_UNTIL`，从而实现线程之间的同步

### 信号量(semaphore)：一种条件变量的特例

```c
void P(sem_t *sem) { // wait
  wait_until(sem->count > 0) {
    sem->count--;
  }
}

void V(sem_t *sem) { // post (signal)
  sem->count++;
}
```

正是因为条件的特殊性，信号量不需要 broadcast

- P 失败时立即睡眠等待
- 执行 V 时，唤醒任意等待的线程

```sh
gcc pc-sem.c && ./a.out
```

#### 两种典型应用

- 实现一次临时的 happens-before
- 实现计数型的同步

对应了两种线程 join 的方法

```sh
gcc join-sem.c && ./a.out
```

```sh
gcc fish-sem.c && ./a.out
```

#### 哲 ♂ 学家吃饭问题

```sh
gcc philosopher.c && ./a.out
```

反思：分布与集中

“Leader/follower” - 有一个集中的 “总控”，而非 “各自协调”

- 在可靠的消息机制上实现任务分派
- Leader 串行处理所有请求 (例如：条件变量服务)

```c
void Tphilosopher(int id) {
  send(Twaiter, id, EAT);
  receive(Twatier); // 等待 waiter 把两把叉子递给哲学家
  eat();
  send(Twaiter, id, DONE); // 归还叉子
}

void Twaiter() {
  while (1) {
    (id, status) = receive(Any);
    switch (status) { ... }
  }
}
```

the Google file system

## 协程(coroutine)：操作系统 “不感知” 的上下文切换

和线程概念相同 (独立堆栈、共享内存)

- 但 “一直执行”，直到 yield() 主动放弃处理器
  - 有编译器辅助，切换开销低
    - yield() 是函数调用，只需保存/恢复 “callee saved” 寄存器
    - 线程切换需要保存/恢复全部寄存器
- 但等待 I/O 时，其他协程就不能运行了……
  - 失去了并行

### Go 和 Goroutine

Goroutine: 概念上是线程，实际是线程和协程的混合体

```sh
go run fib.go
```

```sh
go run pc.go
```

## 真实世界的并发 Bug

### 死锁 (Deadlock)

#### AA-Deadlock

```c
lock(&lk);
// lk = LOCKED;
lock(&lk);
// while (xchg(&lk, LOCKED) == LOCKED) ;
```

#### ABBA-Deadlock

```c
void Tphilosopher() {
  P(&avail[lhs]);
  P(&avail[rhs]);
  // ...
  V(&avail[lhs]);
  V(&avail[rhs]);
}
```

#### 死锁产生的必要条件

- Mutual-exclusion - 一张校园卡只能被一个人拥有
- Wait-for - 一个人等其他校园卡时，不会释放已有的校园卡
- No-preemption - 不能抢夺他人的校园卡
- Circular-chain - 形成校园卡的循环等待关系

打破任何一个即可避免死锁

### 数据竞争（Data Race）

**不同的线程**同时访问**同一内存**，且**至少有一个是写**。

用锁保护好共享数据，消灭一切数据竞争

```c
// Case #1: 上错了锁
void thread1() { spin_lock(&lk1); sum++; spin_unlock(&lk1); }
void thread2() { spin_lock(&lk2); sum++; spin_unlock(&lk2); }
```

```c
// Case #2: 忘记上锁
void thread1() { spin_lock(&lk1); sum++; spin_unlock(&lk1); }
void thread2() { sum++; }
```

### violations

#### 原子性违反 (AV)

ABA

TOCTTOU - time of check to time of use

#### 顺序违反 (OV)

BA

## 并发 Bug 的应对

### defensive programming

### 运行时检查

lockdep

### Sanitizers

```sh
$ gcc -ggdb -fsanitize=thread alipay.c && ./a.out
==================
WARNING: ThreadSanitizer: data race (pid=2603)
  Read of size 8 at 0xaaaaaaab2010 by thread T2:
    #0 Alipay_withdraw /vagrant/concurrency/alipay.c:6 (a.out+0xec0)
    #1 Talipay /vagrant/concurrency/alipay.c:13 (a.out+0xf50)
    #2 wrapper /vagrant/concurrency/thread.h:21 (a.out+0xbe4)

  Previous write of size 8 at 0xaaaaaaab2010 by thread T1:
    #0 Alipay_withdraw /vagrant/concurrency/alipay.c:8 (a.out+0xf08)
    #1 Talipay /vagrant/concurrency/alipay.c:13 (a.out+0xf50)
    #2 wrapper /vagrant/concurrency/thread.h:21 (a.out+0xbe4)

  Location is global 'balance' of size 8 at 0xaaaaaaab2010 (a.out+0x000000012010)

  Thread T2 (tid=2606, running) created by main thread at:
    #0 pthread_create ../../../../src/libsanitizer/tsan/tsan_interceptors_posix.cpp:969 (libtsan.so.0+0x63bb0)
    #1 create /vagrant/concurrency/thread.h:32 (a.out+0xd50)
    #2 main /vagrant/concurrency/alipay.c:18 (a.out+0xf98)

  Thread T1 (tid=2605, finished) created by main thread at:
    #0 pthread_create ../../../../src/libsanitizer/tsan/tsan_interceptors_posix.cpp:969 (libtsan.so.0+0x63bb0)
    #1 create /vagrant/concurrency/thread.h:32 (a.out+0xd50)
    #2 main /vagrant/concurrency/alipay.c:17 (a.out+0xf8c)

SUMMARY: ThreadSanitizer: data race /vagrant/concurrency/alipay.c:6 in Alipay_withdraw
==================
balance = 0
ThreadSanitizer: reported 1 warnings
```

```sh
$ gcc -ggdb -fsanitize=address uaf.c && ./a.out
=================================================================
==2977==ERROR: AddressSanitizer: heap-use-after-free on address 0xffff97f007b0 at pc 0xaaaadb0a09dc bp 0xfffff17af420 sp 0xfffff17af430
WRITE of size 4 at 0xffff97f007b0 thread T0
    #0 0xaaaadb0a09d8 in main /vagrant/concurrency/uaf.c:8
    #1 0xffff9bfe73f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0xffff9bfe74c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0xaaaadb0a082c in _start (/vagrant/concurrency/a.out+0x82c)

0xffff97f007b0 is located 0 bytes inside of 4-byte region [0xffff97f007b0,0xffff97f007b4)
freed by thread T0 here:
    #0 0xffff9c219fe8 in __interceptor_free ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:127
    #1 0xaaaadb0a0988 in main /vagrant/concurrency/uaf.c:7
    #2 0xffff9bfe73f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #3 0xffff9bfe74c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #4 0xaaaadb0a082c in _start (/vagrant/concurrency/a.out+0x82c)

previously allocated by thread T0 here:
    #0 0xffff9c21a2f4 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0xaaaadb0a0920 in main /vagrant/concurrency/uaf.c:5
    #2 0xffff9bfe73f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #3 0xffff9bfe74c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #4 0xaaaadb0a082c in _start (/vagrant/concurrency/a.out+0x82c)

SUMMARY: AddressSanitizer: heap-use-after-free /vagrant/concurrency/uaf.c:8 in main
Shadow bytes around the buggy address:
  0x200ff2fe00a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff2fe00b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff2fe00c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff2fe00d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff2fe00e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x200ff2fe00f0: fa fa fa fa fa fa[fd]fa fa fa fa fa fa fa fa fa
  0x200ff2fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff2fe0110: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff2fe0120: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff2fe0130: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff2fe0140: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==2977==ABORTING
```

### stack guard

#### 烫烫烫、屯屯屯和葺葺葺

- 未初始化栈：`0xcdcccccc`
- 未初始化堆：`0xcdcdcdcd`
- 对象头尾：`0xfdfdfdfd`
- 已回收内存：`0xdddddddd`
  - 手持两把锟斤拷，口中疾呼烫烫烫
  - 脚踏千朵屯屯屯，笑看万物锘锘锘
  - （它们一直在无形中保护你）

```sh
$ python3 -c "print((b'\xcc' * 80).decode('gb2312'))"
烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫

$ python3 -c "print((b'\xcd' * 80).decode('gb2312'))"
屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯屯

$ python3 -c "print((b'\xdd' * 80).decode('gb2312'))"
葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺葺
```
