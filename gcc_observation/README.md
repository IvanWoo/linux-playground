# gcc-observation

- main syscall
    - `execve`
    - `read`
    - `write`
- `strace -f -o a.log gcc a.c`
    - `grep "execve(" a.log | grep -v "ENOENT"`
```sh
3514  execve("/usr/bin/gcc", ["gcc", "a.c"], 0xfffffc3eb470 /* 16 vars */) = 0
3515  execve("/usr/lib/gcc/aarch64-linux-gnu/9/cc1", ["/usr/lib/gcc/aarch64-linux-gnu/9"..., "-quiet", "-imultiarch", "aarch64-linux-gnu", "a.c", "-quiet", "-dumpbase", "a.c", "-mlittle-endian", "-mabi=lp64", "-auxbase", "a", "-fasynchronous-unwind-tables", "-fstack-protector-strong", "-Wformat", "-Wformat-security", "-fstack-clash-protection", "-o", "/tmp/cc4eTZWT.s"], 0x179e640 /* 19 vars */ <unfinished ...>
3516  execve("/usr/bin/as", ["as", "-EL", "-mabi=lp64", "-o", "/tmp/ccU0NMTT.o", "/tmp/cc4eTZWT.s"], 0x179e640 /* 19 vars */ <unfinished ...>
3517  execve("/usr/lib/gcc/aarch64-linux-gnu/9/collect2", ["/usr/lib/gcc/aarch64-linux-gnu/9"..., "-plugin", "/usr/lib/gcc/aarch64-linux-gnu/9"..., "-plugin-opt=/usr/lib/gcc/aarch64"..., "-plugin-opt=-fresolution=/tmp/cc"..., "-plugin-opt=-pass-through=-lgcc", "-plugin-opt=-pass-through=-lgcc_"..., "-plugin-opt=-pass-through=-lc", "-plugin-opt=-pass-through=-lgcc", "-plugin-opt=-pass-through=-lgcc_"..., "--build-id", "--eh-frame-hdr", "--hash-style=gnu", "--as-needed", "-dynamic-linker", "/lib/ld-linux-aarch64.so.1", "-X", "-EL", "-maarch64linux", "--fix-cortex-a53-843419", "-pie", "-z", "now", "-z", "relro", "/usr/lib/gcc/aarch64-linux-gnu/9"..., "/usr/lib/gcc/aarch64-linux-gnu/9"..., "/usr/lib/gcc/aarch64-linux-gnu/9"..., "-L/usr/lib/gcc/aarch64-linux-gnu"..., "-L/usr/lib/gcc/aarch64-linux-gnu"..., "-L/usr/lib/gcc/aarch64-linux-gnu"..., "-L/lib/aarch64-linux-gnu", ...], 0x179e990 /* 21 vars */ <unfinished ...>
3518  execve("/usr/bin/ld", ["/usr/bin/ld", "-plugin", "/usr/lib/gcc/aarch64-linux-gnu/9"..., "-plugin-opt=/usr/lib/gcc/aarch64"..., "-plugin-opt=-fresolution=/tmp/cc"..., "-plugin-opt=-pass-through=-lgcc", "-plugin-opt=-pass-through=-lgcc_"..., "-plugin-opt=-pass-through=-lc", "-plugin-opt=-pass-through=-lgcc", "-plugin-opt=-pass-through=-lgcc_"..., "--build-id", "--eh-frame-hdr", "--hash-style=gnu", "--as-needed", "-dynamic-linker", "/lib/ld-linux-aarch64.so.1", "-X", "-EL", "-maarch64linux", "--fix-cortex-a53-843419", "-pie", "-z", "now", "-z", "relro", "/usr/lib/gcc/aarch64-linux-gnu/9"..., "/usr/lib/gcc/aarch64-linux-gnu/9"..., "/usr/lib/gcc/aarch64-linux-gnu/9"..., "-L/usr/lib/gcc/aarch64-linux-gnu"..., "-L/usr/lib/gcc/aarch64-linux-gnu"..., "-L/usr/lib/gcc/aarch64-linux-gnu"..., "-L/lib/aarch64-linux-gnu", ...], 0xffffc19c0180 /* 21 vars */) = 0
```
    - `grep "execve(" a.log | grep -v "ENOENT" | awk '{print $2}'`
```sh
execve("/usr/bin/gcc",
execve("/usr/lib/gcc/aarch64-linux-gnu/9/cc1",
execve("/usr/bin/as",
execve("/usr/lib/gcc/aarch64-linux-gnu/9/collect2",
execve("/usr/bin/ld",
```

the full pipeline

```
            cc      as      ld
.c ---> .i ---> .s ---> .o ---> a.out
```

## ref

- [应用视角的操作系统](https://jyywiki.cn/OS/2023/build/lect2.ipynb)
