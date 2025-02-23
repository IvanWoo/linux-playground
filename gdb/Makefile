CC = gcc
CFLAGS = -g
SRC = hello.c

.PHONY: all clean

all: a.out

a.out: $(SRC)
	$(CC) $(CFLAGS) $(SRC)

clean:
	rm -f a.out

gdb:
	gdb -x init.gdb a.out
