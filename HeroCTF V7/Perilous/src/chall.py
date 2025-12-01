#!/usr/bin/env python3
from cryptography.hazmat.decrepit.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher
import os

with open("flag.txt", "rb") as f:
    FLAG = f.read()

MASK = os.urandom(len(FLAG))
KEYS = []


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b * (1 + len(a) // len(b))))


def encrypt(k: str, m: str) -> str:
    k = bytes.fromhex(k)
    m = bytes.fromhex(m)

    if k in KEYS:
        raise Exception("Duplicate key used, aborting")

    KEYS.append(k)

    algorithm = algorithms.ARC4(k)
    cipher = Cipher(algorithm, mode=None)
    encryptor = cipher.encryptor()

    m = xor(m, MASK)
    m = encryptor.update(m)
    m = xor(m, MASK)
    return m.hex()


print(
    "Welcome to my RC4 encryption service! Some may call it deprecated, I call it vintage.",
)

k = input("flag k: ")
print(encrypt(k, FLAG.hex()))

while True:
    k = input("k: ")
    m = input("m: ")
    print(encrypt(k, m))
