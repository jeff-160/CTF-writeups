import random

with open('output.txt', 'r') as f:
    enc = bytes.fromhex(f.read().strip())

random.seed(1337)

flag = b""

for byte in enc:
    random_key = random.randint(0, 255)
    flag += bytes([byte ^ random_key])

print("Flag:", flag.decode())