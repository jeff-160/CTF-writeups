import base64

with open("flag.txt") as f:
    flag = f.read().strip()

while "{" not in flag:
    flag = base64.b64decode(flag).decode()

print("Flag:", flag)