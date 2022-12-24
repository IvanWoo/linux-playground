import sys
import os

r, w = os.pipe()

ls_pid = os.fork()
if not ls_pid:
    # child
    os.close(r)
    os.dup2(w, sys.stdout.fileno())
    os.close(w)
    os.execve(
        "/bin/ls",
        [
            "/bin/ls",
            "-la",
        ],
        os.environ,
    )


wc_pid = os.fork()
if not wc_pid:
    # child
    os.close(w)
    os.dup2(r, sys.stdin.fileno())
    os.close(r)
    os.execve("/usr/bin/wc", ["/usr/bin/wc", "-l"], os.environ)


os.close(r)
os.close(w)

for i in range(2):
    pid, status = os.waitpid(-1, 0)
