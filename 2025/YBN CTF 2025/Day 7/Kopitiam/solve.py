from pwn import *
import base58
import string
import re

BIN = './src/kopitiam'

p = process(BIN)

# level 1
a = b'kopi0'
p.sendlineafter(b'[Level 1]', a)

# level 2
def extract(addr, length):
    with open(BIN, 'rb') as f:
        f.seek(addr)

        return f.read(length).rstrip(b'\x00')

key = extract(0x36ab7b, 2)
target = extract(0x36ab70, 11)

decoded = base58.b58decode(target)
b = bytes(decoded[i] ^ key[i & 1] for i in range(len(decoded)))
print(b)

p.sendlineafter(b'[Level 2]', b)

# level 3
target = extract(0x36ab60, 10)

def forward_transform(ch):
    c = ord(ch)

    if (c + 0x9f) & 0xff < 0x1a:
        c = ((c - 0x54) % 26) + ord('a')
    elif (c + 0xbf) & 0xff < 0x1a:
        c = ((c - 0x34) % 26) + ord('A')

    return (c + 3) & 0xff

result = ""

for t in target:
    for ch in string.ascii_letters:
        if forward_transform(ch) == t:
            result += ch
            break

p.sendlineafter(b'[Level 3]', result.encode())

resp = p.recvall().decode()
p.close()

flag = re.findall(r'(YBN25{.+})', resp)[0]
print("Flag:", flag)