key = 0xDC11F1F1

with open("need-for-speed", 'rb') as f:
    f.seek(0x3020)
    enc = list(f.read(55))

flag = enc.copy()

key_bytes = key.to_bytes(4, "little")

for i in range(len(flag)):
    xor_byte = key_bytes[i % 2]
    flag[i] ^= xor_byte
    if i % 3 == 2:
        key = (key + 1) & 0xFFFFFFFF
        key_bytes = key.to_bytes(4, "little")

print("Flag:", bytes(flag).decode())