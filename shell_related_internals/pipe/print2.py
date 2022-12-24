import signal
import os
import sys


def signal_handler(signum, frame):
    print(f"[pipe] signal number: {signum}", file=sys.stderr)
    os._exit(signum)


signal.signal(signal.SIGPIPE, signal_handler)

for i in range(9999):
    print(f"{i}")
