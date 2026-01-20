with open('rev_this', "r") as f:
    enc = f.read().strip()

flag = ''

for i in range(len(enc)):
    if i < 8:
        flag += enc[i]
    elif 8 <= i < 23:
        if i % 2 == 0:
            flag += chr(ord(enc[i]) - 5)
        else:
            flag += chr(ord(enc[i]) + 2)
    else:
        flag += enc[i]

print("Flag:", flag)