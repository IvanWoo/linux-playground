# shell internals

create the required file

```sh
dd if=/dev/random of=/var/tmp/file1.db count=100 bs=1M
```

## [File descriptor and open file description](https://biriukov.dev/docs/fd-pipe-session-terminal/1-file-descriptor-and-open-file-description/)

### tricks

check current process fd `ls -la /proc/$$/fd`

`-` means to read a file content from the stdin, for instance `echo "123" | diff -u /tmp/file1.txt -`

## [Pipes](https://biriukov.dev/docs/fd-pipe-session-terminal/2-pipes/)

one-directional communication channels between related processes (often a parent and a child).

### buffer

buffering all their writes in memory before the actual write syscall executes improve the performance

- block buffer
- liner buffer

### `SIGPIPE` signal

to notify the writer for exiting

### why need pipefail

```sh
$ set -o pipefail
$ echo 'some text' | grep no_such_text | cut -f 1
$ echo $?
1
```

### FIFO or Named pipes

### `pv` tool

- monitor the progress of data through a pipe
- rate-limit for testing

### PIPE Nonblocking I/O

