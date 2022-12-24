import os


with open("/var/tmp/file1.db", "r") as f:
    print(f.fileno())

    print(f"parent {os.getpid()}")
    os.dup2(f.fileno(), 123)

    pid = os.fork()
    if not pid:
        # child
        print(f"child {os.getpid()}")

        # prevent leading the fd from parent to child
        max_fd = os.sysconf("SC_OPEN_MAX")
        os.closerange(3, max_fd)

        os.execve("./sleep.py", ["./sleep.py"], os.environ)

    f.seek(234)
    os.waitpid(-1, 0)
