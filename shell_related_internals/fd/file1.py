import time
import os
import sys

print(f"pid: {os.getpid()}")
with open("/var/tmp/file1.db", "r") as f:
    print(f.fileno())
    f.seek(int(sys.argv[1]))
    time.sleep(99999)
