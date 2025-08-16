from pwn import *

PASSWORD = 0x41A9CC23

p = remote("csd.sentinel-cyber.sg", 32029)

p.sendline(b'START')

p.sendlineafter(b'LOGIN\n', b"USERNAME|john")

challenge = int(p.recvline().decode().split("|")[1].strip())

p.sendline(f'RESPONSE|{challenge ^ PASSWORD}'.encode())

print(p.recvall().decode())