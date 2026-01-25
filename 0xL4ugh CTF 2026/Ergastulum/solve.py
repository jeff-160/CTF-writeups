from pwn import *

io = remote("challenges3.ctf.sd", 33808)

with open("payload.py") as f:
    payload = f.read().strip()

io.recvuntil(b'send')

for line in payload.split('\n'):
    io.sendline(line.encode())

io.sendline(b'end')
io.interactive()