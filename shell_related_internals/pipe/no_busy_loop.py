import os

rand = os.getrandom(1 << 16 - 1)

while True:
    os.write(1, rand)
