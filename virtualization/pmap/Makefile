CC = gcc
CFLAGS = -g

.PHONY: all clean

all: a.out

a.out: hello.c
	$(CC) $(CFLAGS) hello.c

clean:
	rm -f a.out

gdb:
	gdb -x init.gdb a.out
