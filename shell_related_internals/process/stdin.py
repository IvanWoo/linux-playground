import fileinput
import signal
import os
import sys


def signal_handler(signum, frame):
    print(f"[stdin] signal number: {signum}", file=sys.stderr)
    os._exit(signum)


signal.signal(signal.SIGTERM, signal_handler)


for i, line in enumerate(fileinput.input()):
    print(f"{i+1}: {line.rstrip()}")
