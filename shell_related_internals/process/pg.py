import os
import time
import signal


print(f"parent: {os.getpid()}")
pgpid = os.fork()
if not pgpid:
    # child
    os.setpgid(os.getpid(), os.getpid())
    os.execve(
        "./sleep.py",
        [
            "./sleep.py",
        ],
        os.environ,
    )

print(f"pgid: {pgpid}")

pid = os.fork()
if not pid:
    # child
    os.setpgid(os.getpid(), pgpid)
    os.execve(
        "./sleep.py",
        [
            "./sleep.py",
        ],
        os.environ,
    )


pid = os.fork()
if not pid:
    # child
    os.setpgid(os.getpid(), pgpid)
    os.execve(
        "./sleep.py",
        [
            "./sleep.py",
        ],
        os.environ,
    )


tty_fd = os.open("/dev/tty", os.O_RDONLY)

os.tcsetpgrp(tty_fd, pgpid)

for i in range(3):
    os.waitpid(-1, 0)

h = signal.signal(signal.SIGTTOU, signal.SIG_IGN)
os.tcsetpgrp(tty_fd, os.getpgrp())
signal.signal(signal.SIGTTOU, h)

print("got foreground back")

time.sleep(99999)
