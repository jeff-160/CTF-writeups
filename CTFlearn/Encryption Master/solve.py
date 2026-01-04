import base64
import re

with open("Here ya go!.txt", 'r') as f:
    enc = f.read()

enc = base64.b64decode(re.findall(r'fun. (.+)', enc)[0].strip()).decode()
enc = bytes.fromhex(re.findall(r'going. (.+)', enc)[0].strip()).decode()
enc = "".join(chr(int(b, 2)) for b in re.findall(r'more. (.+)', enc)[0].strip().split())

flag = base64.b64decode(re.findall(r'! (.+)', enc)[0].strip()).decode()
print("Flag:", flag)