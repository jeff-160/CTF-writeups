import re

with open("stream.bin", "rb") as f:
    flags = re.findall(r'(picoCTF{.+})', f.read().decode(errors='ignore'))

print("Flag:", flags[-1])