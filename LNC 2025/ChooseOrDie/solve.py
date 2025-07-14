import hashlib
import base64

target_hash = base64.b64decode("LNSg2cOUwwiVgmq4nKdWBA==")

values = [6, 7]

for i in range(2 ** 16):
    buffer = bytearray(16)
    for j in range(16):
        bit = (i >> j) & 1
        buffer[j] = values[bit]

    input_hash = hashlib.md5(buffer).digest()

    if input_hash == target_hash:
        seq = ['Yes' if b == 6 else 'No' for b in buffer]
        print("Found matching sequence!")
        print(seq)
