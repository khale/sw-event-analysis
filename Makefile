CC:=gcc
CFLAGS:= -02 -Wall 

%.o: %.c
	$(CC) -o 

clean:
	@rm -f *.o
