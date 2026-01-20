with open("encoded.bmp", "rb") as f:
    f.seek(2000)
    data = f.read(50 * 8)

flag = ""

for i in range(50):
    c = 0
    for bit in range(8):
        lsb = data[i * 8 + bit] & 1
        c |= (lsb << bit)
    flag += chr(c + 5)

print("Flag:", flag)