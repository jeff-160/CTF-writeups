from pwn import *
from cryptography.hazmat.decrepit.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher

def rc4_keystream(key, n):
    cipher = Cipher(algorithms.ARC4(key), mode=None)
    encryptor = cipher.encryptor()
    return encryptor.update(b"\x00" * n)

r = remote("crypto.heroctf.fr", 9001)
r.recvuntil(b"flag k:")

key = b"00112233445566778899aabbccddeeff"  
r.sendline(key.decode())

enc = bytes.fromhex(r.recvline().strip().decode())

ks = rc4_keystream(bytes.fromhex(key.decode()), len(enc))

flag = bytes(x ^ y for x, y in zip(enc, ks))
print("Flag:", flag.decode())