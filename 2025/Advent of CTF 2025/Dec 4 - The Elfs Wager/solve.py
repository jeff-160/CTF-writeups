offset = 0x2110
length = 0x17

with open("src/day4", "rb") as f:
    f.seek(offset)

    enc = f.read(length)

flag = bytes([b ^ 0x42 for b in enc])

print(flag.decode())