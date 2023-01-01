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

```sh
mkfifo hello
```

The FIFO file could be helpful when you need to build a connection between completely unrelated programs or daemons without changing their source code.

### `pv` tool

- monitor the progress of data through a pipe
- rate-limit for testing

### PIPE Nonblocking I/O

## [process groups, jobs and sessions](https://biriukov.dev/docs/fd-pipe-session-terminal/3-process-groups-jobs-and-sessions/)

### process groups

process group is job

a process group lives as long as it has at least one member

how to leave a process group:

- join another group
- creating its own new group
- terminate

sends a SIGTERM(15) to all members of the process group 123(the dash in front of 123 matters)

```sh
kill -15 -123
```

### sessions

a session is a collection of process groups

get the stats of current running process

```sh
cat /proc/$$/stat | cut -d " " -f 1,4,5,6,7,8 | tr ' ' '\n' | paste <(echo -ne "pid\nppid\npgid\nsid\ntty\ntgid\n") -
```

### shell job control

move this job to the background by pressing `Ctrl+Z`

check job status: `jobs -l`

resume background job: `bg %1`

move job to foreground: `fg %1`

start a job in background by adding an ampersand (`&`) char in the end of the pipeline: `sleep 999 | grep 123 &`

### `kill` command

### `nohup` and `disown`

to protect our long-running program from being suddenly killed by a broken internet connection or low laptop battery
make the program immune to the `SIGHUP` signal

e.g

```sh
nohup ./sleep.py &
```

```sh
./sleep.py &
jobs -l
disown <pid>
```

### Daemons

long living process

The classic “unix” way of spawning daemons is performed by a double-fork technique
but nowadays developers rely on the `systemd` features

## [Terminals and pseudoterminals](https://biriukov.dev/docs/fd-pipe-session-terminal/4-terminals-and-pseudoterminals/)

### pseudoterminals(`dev/pts`)

### terminal settings

```sh
stty -a
```

### terminal signals

### `screen` and `tmux`

```sh
tmux attach
tmux detach
```

```sh
pstree -p
```

### pseudoterminal proxy

`expect`

uses a pseudoterminal to allow an interactive terminal-oriented program to be driven from a script file.

```sh
#!/usr/bin/expect

set timeout 20

set host [lindex $argv 0]
set username [lindex $argv 1]
set password [lindex $argv 2]

spawn ssh "$username\@$host"

expect "password:"
send "$password\r";

interact
```

`script`

```sh
script --timing=time.txt script.log
```

```sh
scriptreplay --timing=time.txt script.log
```

[`reptyr`](https://github.com/nelhage/reptyr)

on one terminal

```sh
# any long running process forget to run inside a tmux
htop
```

on the other terminal

```sh
tmux
ps -a
reptyr <htop pid>
```

Detach your terminal multiplexer `CTRL-B D`
