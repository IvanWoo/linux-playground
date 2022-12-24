import time
import sys


print("start sleeping", file=sys.stderr)
time.sleep(30)
print("stop sleeping", file=sys.stderr)

r = sys.stdin.buffer.read(4096)
while len(r) > 0:
    r = sys.stdin.buffer.read(4096)

print("finished reading", file=sys.stderr)
