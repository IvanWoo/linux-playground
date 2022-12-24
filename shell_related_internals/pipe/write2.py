import signal
import sys
import os


def signal_handler(signum, frame):
    print(f"signal {signum} {frame}", file=sys.stderr)


signal.signal(signal.SIGUSR1, signal_handler)

print(os.getpid(), file=sys.stderr)

rand = os.getrandom(1 << 29)
print("generated", file=sys.stderr)

n = os.write(1, rand)

print(f"written: {n}", file=sys.stderr)
