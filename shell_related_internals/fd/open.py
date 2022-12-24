import os
import sys
import time

file_path = sys.argv[1]

print(os.getpid())
fd = os.open(file_path, os.O_APPEND | os.O_RSYNC | os.O_NOATIME)
with os.fdopen(fd, "r+") as f:
    print(f.fileno())
    time.sleep(9999)
