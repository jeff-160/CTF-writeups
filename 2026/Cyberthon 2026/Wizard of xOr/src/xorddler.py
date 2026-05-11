import os
import secrets

FLAG = os.environ['FLAG']
front_pad = secrets.randbits(8)
back_pad = secrets.randbits(8)
FLAG = secrets.token_bytes(front_pad) + FLAG.encode() + secrets.token_bytes(back_pad)
XOR_KEY = secrets.token_bytes(8)
print(f"XOR_KEY: {XOR_KEY.hex().upper()}\nFLAG: {FLAG}")

CIPHERTEXT = [FLAG[i] ^ XOR_KEY[i % len(XOR_KEY)] for i in range(len(FLAG))]
open("ciphertext.bin", "wb").write(bytes(CIPHERTEXT))
