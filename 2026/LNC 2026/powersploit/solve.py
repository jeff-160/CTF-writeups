from pwn import *

io = remote("chall1.lagncra.sh", 18339)

with open("answers.txt", "r") as f:
    lines = f.read().split('\n')

for line in lines:
    io.sendlineafter(b'>', line.encode())

io.interactive()