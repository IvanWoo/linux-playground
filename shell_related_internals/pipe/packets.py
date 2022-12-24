import sys
import os
import time


PIPE_BUF = 4096

print(f"supervisor: {os.getpid()}", file=sys.stderr)

r, w = os.pipe2(os.O_DIRECT)

# fork 2 writers
for instance in range(2):
    writer_pid = os.fork()
    if not writer_pid:
        print(f"writer{instance}: {os.getpid()}", file=sys.stderr)

        os.close(r)
        pid = os.getpid()
        for i in range(100):
            os.write(w, f"writer{instance}: {i}".encode())
            time.sleep(1)

# fork 2 readers
for instance in range(2):
    reader_pid = os.fork()
    if not reader_pid:
        print(f"reader{instance}: {os.getpid()}", file=sys.stderr)

        os.close(w)
        pid = os.getpid()
        for i in range(100):
            data = os.read(r, PIPE_BUF)
            if not len(data):
                break
            print(f"reader{instance}: {data}")

os.close(r)
os.close(w)

for i in range(4):
    os.waitpid(-1, 0)
