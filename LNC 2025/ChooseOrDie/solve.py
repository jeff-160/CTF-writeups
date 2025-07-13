import hashlib
import base64

target_b64 = "LNSg2cOUwwiVgmq4nKdWBA=="
target_md5 = base64.b64decode(target_b64)

def md5_of_buffer(buf):
    return hashlib.md5(buf).digest()

values = [6, 7]

for i in range(2 ** 16):
    buffer = bytearray(16)
    for j in range(16):
        bit = (i >> j) & 1
        buffer[j] = values[bit]

    if md5_of_buffer(buffer) == target_md5:
        seq = ['Yes' if b == 6 else 'No' for b in buffer]
        print("Found matching sequence!")
        print(seq)