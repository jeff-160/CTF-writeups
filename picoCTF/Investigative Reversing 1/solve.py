def extract(img, length):
    with open(img, "rb") as f:
        return f.read()[-length:]

flag1 = extract("mystery.png", 16)
flag2 = extract("mystery2.png", 2)
flag3 = extract("mystery3.png", 8)

flag = [0] * 26

# mystery2.png
flag[0] = flag2[0] - 0x15
flag[3] = flag2[1] - 4

# mystery3.png
flag[1] = flag3[0]
flag[2] = flag3[1]
flag[5] = flag3[2]
flag[10] = flag3[3]
flag[11] = flag3[4]
flag[12] = flag3[5]
flag[13] = flag3[6]
flag[14] = flag3[7]

# mystery.png
flag[4] = flag1[0]
flag[6] = flag1[1]
flag[7] = flag1[2]
flag[8] = flag1[3]
flag[9] = flag1[4]

for i in range(15, 26):
    flag[i] = flag1[i - 10]

print("Flag:", bytes(flag).decode())