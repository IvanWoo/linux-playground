import os
import sys


pid = sys.argv[1]
fd = sys.argv[2]


with open(f"/proc/{pid}/fdinfo/{fd}", "r") as f:
    flags = f.readlines()[1].split("\t")[1].strip()

    print(f"Flags mask: {flags}")

    flags = int(flags, 8)

    # check status flags
    if flags & os.O_RDONLY:
        print("os.O_RDONLY is set")
    if flags & os.O_WRONLY:
        print("os.O_WRONLY is set")
    if flags & os.O_RDWR:
        print("os.O_RDWR is set")
    if flags & os.O_APPEND:
        print("os.O_APPEND is set")
    if flags & os.O_DSYNC:
        print("os.O_DSYNC is set")
    if flags & os.O_RSYNC:
        print("os.O_RSYNC is set")
    if flags & os.O_SYNC:
        print("os.O_SYNC is set")
    if flags & os.O_NDELAY:
        print("os.O_NDELAY is set")
    if flags & os.O_NONBLOCK:
        print("os.O_NONBLOCK is set")
    if flags & os.O_ASYNC:
        print("os.O_ASYNC is set")
    if flags & os.O_DIRECT:
        print("os.O_DIRECT is set")
    if flags & os.O_NOATIME:
        print("os.O_NOATIME is set")
    if flags & os.O_PATH:
        print("os.O_PATH is set")

    # check close on exec
    if flags & os.O_CLOEXEC:
        print("os.O_CLOEXEC is set")
