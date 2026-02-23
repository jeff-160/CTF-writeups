import base64

with open("start.txt", "r") as f:
    enc = f.read().replace(" ", "")

enc = ''.join(chr(int(enc[i : i + 8], 2)) for i in range(0, len(enc), 8))

enc = bytes.fromhex(enc).decode()

flag = base64.b64decode(enc).decode()

print("Flag:", flag)