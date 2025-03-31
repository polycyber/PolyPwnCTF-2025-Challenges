CC = gcc
CFLAGS = -s -Wall -O0 -no-pie -fno-stack-protector -static
LIBC = libc.a
GADGET_S = gadget.s
SERVER_SRC = server.c
CLIENT_SRC = client.c
SERVER_BIN = server
CLIENT_BIN = client

all: $(SERVER_BIN) $(CLIENT_BIN)

$(SERVER_BIN): $(SERVER_SRC) $(GADGET_S)
	$(CC) $(CFLAGS) -o $(SERVER_BIN) $(SERVER_SRC) $(GADGET_S)

$(CLIENT_BIN): $(CLIENT_SRC)
	$(CC) $(CFLAGS) -o $(CLIENT_BIN) $(CLIENT_SRC)

clean:
	rm -f $(SERVER_BIN) $(CLIENT_BIN)

.PHONY: all clean
