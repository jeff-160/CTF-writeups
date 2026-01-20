def decrypt(data):
    out = bytearray(26)

    out[0:6] = data[0:6]

    for i in range(6, 15):
        out[i] = (data[i] - 5) & 0xff

    out[15] = (data[15] + 3) & 0xff

    out[16:26] = data[16:26]

    return bytes(out)

with open('mystery.png', 'rb') as f:
    contents = f.read()

enc = contents[contents.index(b'pico'):]

flag = decrypt(enc).decode()
print("Flag:", flag)