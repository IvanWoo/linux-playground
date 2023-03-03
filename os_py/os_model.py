#!/usr/bin/env python3

import random
import sys
from pathlib import Path


class OperatingSystem:
    """A minimum executable operating system model."""

    SYSCALLS = ["choose", "write", "spawn", "sched"]

    class Thread:
        """A 'freezed' thread state."""

        def __init__(self, func, *args):
            self._func = func(*args)
            self.retval = None

        def step(self):
            """Proceed with the thread until its next trap."""
            syscall, args, *_ = self._func.send(self.retval)
            self.retval = None
            return syscall, args

    def __init__(self, src):
        variables = {}
        exec(src, variables)
        self._main = variables["main"]

    def run(self):
        threads = [OperatingSystem.Thread(self._main)]
        while threads:
            try:
                match (t := threads[0]).step():
                    case "choose", xs:
                        t.retval = random.choice(xs)
                    case "write", xs:
                        print(xs, end="")
                    case "spawn", (fn, args):
                        threads.append(OperatingSystem.Thread(fn, args))
                    case "sched", _:
                        random.shuffle(threads)
            except StopIteration:
                threads.remove(t)
                random.shuffle(threads)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} file")
        exit(1)

    src = Path(sys.argv[1]).read_text()
    for syscall in OperatingSystem.SYSCALLS:
        src = src.replace(f"sys_{syscall}", f"yield '{syscall}', ")

    OperatingSystem(src).run()
