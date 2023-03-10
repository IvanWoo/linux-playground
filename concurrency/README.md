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