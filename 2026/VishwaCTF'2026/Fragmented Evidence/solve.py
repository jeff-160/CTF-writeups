import re
import base64

with open("server.log", 'r') as f:
    contents = f.read()

strings = re.findall(r'[id|failed]=(.+)', contents)
b64 = ''.join(strings)

print("Flag:", base64.b64decode(b64).decode())  # replace flag{} with VishwaCTF{}