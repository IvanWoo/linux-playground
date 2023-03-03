def number():
    i = 1
    while True:
        ret = yield (f"{i:b}")
        i += ret


def main():
    n = number()
    # start the generator: `next(n)` will do the same thing
    n.send(None)
    for i in range(4):
        print(n.send(i))


main()
