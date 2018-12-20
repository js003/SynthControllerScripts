CC=gcc
CFLAGS = -g 

all: udp-recv

udp-recv: udp-recv.o 
	$(CC) -o udp-recv udp-recv.o $(LIBS)

udp-recv.o: udp-recv.c

clean:
	rm -f udp-recv udp-recv.o 
