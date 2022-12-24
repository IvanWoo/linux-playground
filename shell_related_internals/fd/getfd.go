package main

import (
	"fmt"
	"os"
	"strconv"
	"syscall"
	"time"
)

const (
	sys_pidfd_open  = 434 // from kernel table
	sys_pidfd_getfd = 438
)

func pidfd_open(pid int) (int, error) {
	r1, _, err := syscall.Syscall(sys_pidfd_open, uintptr(pid), 0, 0)
	if err != 0 {
		return -1, err
	}
	return int(r1), nil
}

func pidfd_getfd(pidfd, targetfd int) (int, error) {
	r1, _, err := syscall.Syscall(sys_pidfd_getfd, uintptr(pidfd), uintptr(targetfd), 0)
	if err != 0 {
		return -1, err
	}
	return int(r1), nil
}

func main() {
	var (
		pid, fd int
		err     error
	)

	pid, err = strconv.Atoi(os.Args[1])
	fd, err = strconv.Atoi(os.Args[2])
	if err != nil {
		panic(err)
	}

	fmt.Println("pid:", os.Getpid())

	pidfd, err := pidfd_open(pid)

	if err != nil {
		panic(err)
	}

	newFd, err := pidfd_getfd(pidfd, fd)
	if err != nil {
		panic(err)
	}
	fmt.Println(newFd)

	time.Sleep(time.Hour)
}
