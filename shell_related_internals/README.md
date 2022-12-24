# [What every SRE should know about GNU/Linux shell related internals: file descriptors, pipes, terminals, user sessions, process groups and daemons](https://biriukov.dev/docs/fd-pipe-session-terminal/0-sre-should-know-about-gnu-linux-shell-related-internals-file-descriptors-pipes-terminals-user-sessions-process-groups-and-daemons/)

create the required file

```sh
dd if=/dev/random of=/var/tmp/file1.db count=100 bs=1M
```

## [1. File descriptor and open file description](https://biriukov.dev/docs/fd-pipe-session-terminal/1-file-descriptor-and-open-file-description/)

### tricks

check current process fd `ls -la /proc/$$/fd`

`-` means to read a file content from the stdin, for instance `echo "123" | diff -u /tmp/file1.txt -`
