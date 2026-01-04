from pwn import *
from randcrack import RandCrack
import re

r = remote("138.197.193.132", 5002)

# leak prng numbers
leaked = []

for i in range(624):
    r.sendlineafter(b'>>>', b'R')

    r.recvline()

    rand = re.findall(r'based on (.+)', r.recvline().decode())[0].strip()
    leaked.append(int(rand))
    
    print(f"Leaked: {rand:<10} | {len(leaked)}/624")

# win
rc = RandCrack()

for leak in leaked:
    rc.submit(leak)

moves = {
    0: 'R',
    1: 'P',
    2: 'S'
}

counter = {
    'R': 'P',
    'P': 'S',
    'S': 'R'
}

for i in range(1, 30 + 1):
    print(f"Round {i}/30")

    pred = rc.predict_getrandbits(32)
    choice = counter[moves[pred % 3]]
    r.sendlineafter(b'>>>', choice.encode())

    if b'won' not in r.recvline():
        print("something went wrong")
        r.close()
        exit()

resp = r.recvall().decode()
r.close()

flag = re.findall(r'(CTFlearn{.+})', resp)[0]
print("Flag:", flag)