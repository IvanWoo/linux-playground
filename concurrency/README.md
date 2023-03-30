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
