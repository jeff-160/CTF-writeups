from pwn import *

p = remote("csd.sentinel-cyber.sg", 1337)

p.sendline(b"START")

p.sendlineafter(b'LOGIN', b'USERNAME|john')

print(p.recvall().decode())