import signal
import os
import sys
import time


def signal_handler(signum, frame):
    print(f"[print] signal number: {signum}", file=sys.stderr)
    os._exit(signum)


signal.signal(signal.SIGTERM, signal_handler)

print(f"PGID: {os.getpgrp()}", file=sys.stderr)

for i in range(9999):
    print(f"{i}")
    sys.stdout.flush()
    time.sleep(1)
