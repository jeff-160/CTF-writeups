import re
import base64

with open('TLSB', "rb") as f:
    data = f.read()

pixel_data = data[54:]

bits = []

for byte in pixel_data:
    bit = (byte >> 2) & 1
    bits.append(bit)

message_bytes = []
for i in range(0, len(bits), 8):
    byte_bits = bits[i:i+8]
    if len(byte_bits) < 8:
        break

    value = 0
    for bit in byte_bits:
        value = (value << 1) | bit

    message_bytes.append(value)

message = bytes(message_bytes).decode()

flag = re.findall(r"Flag is: `(.+)'", message)[0]

print("Flag:", base64.b64decode(flag).decode())