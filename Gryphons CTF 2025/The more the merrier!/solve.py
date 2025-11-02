import codecs
import base64
from PIL import Image

enc = '''vIOBEj0XTtbNNNNAFHuRHtNNNZtNNNOxPNNNNNQz7FQKNNNNoRyRDIE4aB3A2j3RVNjRjA3+v3L+
VUPc4JnDDZnicRancxaFMc3f/331W9p2oqezsq/rSrszpxe2fWk8C3A3mj3KaeAke0l/9Kq/x2oF
GWAWM02MAsFnNNNNNNNNNNNNNNNNNNNNNNNNNClgOmFXOzLJBr/ONNNNNRySGxFhDzPP'''

# decrypt cipher text and save as png
rot13 = codecs.decode(enc, 'rot13')
b64 = base64.b64decode(rot13)

with open("out.png", "wb") as f:
    f.write(b64)

# lsb steganography
img = Image.open("out.png")
pixels = list(img.getdata())

bits = [v & 1 for px in pixels for v in (px if isinstance(px, tuple) else (px,))]
data = bytes(int(''.join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8))

print(data.decode('utf-8', errors='ignore'))