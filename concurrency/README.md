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