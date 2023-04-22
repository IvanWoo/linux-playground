# virtualization

## process

因为 “程序 = 状态机”，操作系统上进程 (运行的程序) 管理的 API 很自然地就是状态机的管理。
在 UNIX/Linux 世界中，这是通过以下三个最重要的系统调用实现的：

- fork: 对当前状态机状态进行完整复制
- execve: 将当前状态机状态重置为某个可执行文件描述的状态机
- exit: 销毁当前状态机

## address spaces

查看进程的地址空间

start target program via gdb

```sh
make
make gdb
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
