import fileinput

for i, line in enumerate(fileinput.input()):
    print(f"{i+1}: {line.rstrip()}")
