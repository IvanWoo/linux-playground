import time
import os
import sys


with open("/var/tmp/file1.db", "r") as f:
    print(f.fileno())

    print(f"parent pid: {os.getpid()}")
    pid = os.fork()
    if not pid:
        # child
        print(f"child pid: {os.getpid()}")
        f.seek(int(sys.argv[1]))
        time.sleep(99999)

    os.waitpid(pid, 0)
