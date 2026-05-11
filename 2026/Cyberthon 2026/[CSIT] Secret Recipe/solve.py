from base64 import b64decode
import re

def rc4(data, key):
    key = key.encode('utf-8')
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    result = []
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        result.append(byte ^ K)
    return bytes(result)

with open('magic_potion.enc', 'rb') as f:
    data = f.read()

ct = rc4(data, 'DESKTOP-H3KMT1M')
pt = b64decode(ct).decode()

flag = re.findall(r'encoded as (.+?),', pt)[0].strip()
print("Flag:", b64decode(flag).decode())