import time
import signal
import termios
import fcntl
import struct


def signal_handler(signum, frame):
    packed = fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack("HHHH", 0, 0, 0, 0))
    rows, cols, h_pixels, v_pixels = struct.unpack("HHHH", packed)
    print(rows, cols, h_pixels, v_pixels)


signal.signal(signal.SIGWINCH, signal_handler)

time.sleep(9999)
