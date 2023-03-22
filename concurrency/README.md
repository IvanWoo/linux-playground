# concurrency

## stack size

```sh
gcc stack-prob.c && ./a.out
```

around `8192 KB` == `8 MB`

## challenges of multi-core execuation

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

### no visbility between cpus

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
