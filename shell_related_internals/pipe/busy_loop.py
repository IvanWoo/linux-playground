import os
import fcntl

flags = fcntl.fcntl(1, fcntl.F_GETFL, 0)
fcntl.fcntl(1, fcntl.F_SETFL, flags | os.O_NONBLOCK)

rand = os.getrandom(1 << 16 - 1)

while True:
    try:
        n = os.write(1, rand)
    except BlockingIOError:
        continue
