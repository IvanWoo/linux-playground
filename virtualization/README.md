# virtualization

## process

因为 “程序 = 状态机”，操作系统上进程 (运行的程序) 管理的 API 很自然地就是状态机的管理。
在 UNIX/Linux 世界中，这是通过以下三个最重要的系统调用实现的：

- fork: 对当前状态机状态进行完整复制
- execve: 将当前状态机状态重置为某个可执行文件描述的状态机
- exit: 销毁当前状态机

## address spaces

### 查看进程的地址空间

start target program via gdb

```sh
cd pmap
make
make gdb
```

```sh
(gdb) info proc mappings
process 2290
Mapped address spaces:

          Start Addr           End Addr       Size     Offset  Perms  objfile
      0xaaaaaaaa0000     0xaaaaaaaa1000     0x1000        0x0  r-xp   /vagrant/virtualization/pmap/a.out
      0xaaaaaaab0000     0xaaaaaaab2000     0x2000        0x0  rw-p   /vagrant/virtualization/pmap/a.out
      0xfffff7fc2000     0xfffff7fed000    0x2b000        0x0  r-xp   /usr/lib/aarch64-linux-gnu/ld-linux-aarch64.so.1
      0xfffff7ff9000     0xfffff7ffb000     0x2000        0x0  r--p   [vvar]
      0xfffff7ffb000     0xfffff7ffc000     0x1000        0x0  r-xp   [vdso]
      0xfffff7ffc000     0xfffff8000000     0x4000    0x2a000  rw-p   /usr/lib/aarch64-linux-gnu/ld-linux-aarch64.so.1
      0xfffffffdf000    0x1000000000000    0x21000        0x0  rw-p   [stack]
```

```sh
(gdb) info proc
process 68815
cmdline = '/vagrant/virtualization/a.out'
cwd = '/vagrant/virtualization'
exe = '/vagrant/virtualization/a.out'
(gdb) !pmap 68815
68815:   /vagrant/virtualization/a.out
0000aaaaaaaa0000      4K r-x-- a.out
0000aaaaaaab0000      8K rw--- a.out
0000fffff7fc2000    172K r-x-- ld-linux-aarch64.so.1
0000fffff7ff9000      8K r----   [ anon ]
0000fffff7ffb000      4K r-x--   [ anon ]
0000fffff7ffc000     16K rw--- ld-linux-aarch64.so.1
0000fffffffdf000    132K rw---   [ stack ]
 total              344K
(gdb) !cat /proc/68815/maps
aaaaaaaa0000-aaaaaaaa1000 r-xp 00000000 00:31 240                        /vagrant/virtualization/a.out
aaaaaaab0000-aaaaaaab2000 rw-p 00000000 00:31 240                        /vagrant/virtualization/a.out
fffff7fc2000-fffff7fed000 r-xp 00000000 fd:00 652870                     /usr/lib/aarch64-linux-gnu/ld-linux-aarch64.so.1
fffff7ff9000-fffff7ffb000 r--p 00000000 00:00 0                          [vvar]
fffff7ffb000-fffff7ffc000 r-xp 00000000 00:00 0                          [vdso]
fffff7ffc000-fffff8000000 rw-p 0002a000 fd:00 652870                     /usr/lib/aarch64-linux-gnu/ld-linux-aarch64.so.1
fffffffdf000-1000000000000 rw-p 00000000 00:00 0                         [stack]
(gdb)
```

验证 pmap 是通过访问 procfs (/proc/) 实现的

```sh
strace -f -o pmap.log pmap 68815

grep "/proc/" pmap.log
69743 openat(AT_FDCWD, "/proc/self/auxv", O_RDONLY) = 3
69743 openat(AT_FDCWD, "/proc/sys/kernel/osrelease", O_RDONLY) = 3
69743 openat(AT_FDCWD, "/proc/self/auxv", O_RDONLY) = 3
69743 openat(AT_FDCWD, "/proc/self/maps", O_RDONLY) = 3
69743 newfstatat(AT_FDCWD, "/proc/self/task", {st_mode=S_IFDIR|0555, st_size=0, ...}, 0) = 0
69743 newfstatat(AT_FDCWD, "/proc/68815", {st_mode=S_IFDIR|0555, st_size=0, ...}, 0) = 0
69743 openat(AT_FDCWD, "/proc/68815/stat", O_RDONLY) = 3
69743 openat(AT_FDCWD, "/proc/68815/cmdline", O_RDONLY) = 3
69743 openat(AT_FDCWD, "/proc/68815/maps", O_RDONLY) = 3
```

### 进程地址空间管理

```c
// 映射
void *mmap(void *addr, size_t length, int prot, int flags,
           int fd, off_t offset);
int munmap(void *addr, size_t length);

// 修改映射权限
int mprotect(void *addr, size_t length, int prot);
```

## ELF (Executable and Linkable Format)

```sh
cd elf
gcc ansi.c
```

```sh
ldd a.out

        linux-vdso.so.1 (0x0000ffff964bc000)
        libc.so.6 => /lib/aarch64-linux-gnu/libc.so.6 (0x0000ffff962c0000)
        /lib/ld-linux-aarch64.so.1 (0x0000ffff96483000)
```

### PLT (Procedure Linkage Table)

```sh
objdump -d a.out | grep plt

Disassembly of section .plt:
0000000000000610 <.plt>:
0000000000000630 <__libc_start_main@plt>:
0000000000000640 <__cxa_finalize@plt>:
0000000000000650 <__gmon_start__@plt>:
0000000000000660 <abort@plt>:
0000000000000670 <printf@plt>:
0000000000000680 <putchar@plt>:
 6ec:   97ffffd1        bl      630 <__libc_start_main@plt>
 6f0:   97ffffdc        bl      660 <abort@plt>
 700:   17ffffd4        b       650 <__gmon_start__@plt>
 7ac:   97ffffa5        bl      640 <__cxa_finalize@plt>
 82c:   97ffff91        bl      670 <printf@plt>
 854:   97ffff8b        bl      680 <putchar@plt>
```

```sh
readelf -l a.out

Elf file type is DYN (Position-Independent Executable file)
Entry point 0x6c0
There are 9 program headers, starting at offset 64

Program Headers:
  Type           Offset             VirtAddr           PhysAddr
                 FileSiz            MemSiz              Flags  Align
  PHDR           0x0000000000000040 0x0000000000000040 0x0000000000000040
                 0x00000000000001f8 0x00000000000001f8  R      0x8
  INTERP         0x0000000000000238 0x0000000000000238 0x0000000000000238
                 0x000000000000001b 0x000000000000001b  R      0x1
      [Requesting program interpreter: /lib/ld-linux-aarch64.so.1]
  LOAD           0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000994 0x0000000000000994  R E    0x10000
  LOAD           0x0000000000000d88 0x0000000000010d88 0x0000000000010d88
                 0x0000000000000288 0x0000000000000290  RW     0x10000
  DYNAMIC        0x0000000000000d98 0x0000000000010d98 0x0000000000010d98
                 0x00000000000001f0 0x00000000000001f0  RW     0x8
  NOTE           0x0000000000000254 0x0000000000000254 0x0000000000000254
                 0x0000000000000044 0x0000000000000044  R      0x4
  GNU_EH_FRAME   0x00000000000008a8 0x00000000000008a8 0x00000000000008a8
                 0x000000000000003c 0x000000000000003c  R      0x4
  GNU_STACK      0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000000 0x0000000000000000  RW     0x10
  GNU_RELRO      0x0000000000000d88 0x0000000000010d88 0x0000000000010d88
                 0x0000000000000278 0x0000000000000278  R      0x1

 Section to Segment mapping:
  Segment Sections...
   00
   01     .interp
   02     .interp .note.gnu.build-id .note.ABI-tag .gnu.hash .dynsym .dynstr .gnu.version .gnu.version_r .rela.dyn .rela.plt .init .plt .text .fini .rodata .eh_frame_hdr .eh_frame
   03     .init_array .fini_array .dynamic .got .data .bss
   04     .dynamic
   05     .note.gnu.build-id .note.ABI-tag
   06     .eh_frame_hdr
   07
   08     .init_array .fini_array .dynamic .got
```

### LD_PRELOAD

```sh
cd virtualization/elf && make hook.so
LD_PRELOAD=./hook.so python3 -c "print(2*1e10)" 2>&1 | grep malloc | less
```

## implementation of process

厉害的操作系统，同一份代码仅有一个副本

```sh
cd virtualization && gcc vm.c
```

run multiple programs and verify that `main` and `printf` have the identical physical address among all programs
