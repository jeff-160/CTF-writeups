import re

with open("ciphertext.bin", "rb") as f:
    ct = f.read()

KNOWN = b"Cyberthon"
KEY_LEN = 8

for offset in range(len(ct) - len(KNOWN)):
    key = [None] * KEY_LEN

    for i, ch in enumerate(KNOWN):
        k = ct[offset + i] ^ ch
        pos = (offset + i) % KEY_LEN

        if key[pos] is None:
            key[pos] = k
        elif key[pos] != k:
            break
    else:
        for i in range(KEY_LEN):
            if key[i] is None:
                key[i] = 0

        key = bytes(key)

        pt = bytes(ct[i] ^ key[i % KEY_LEN] for i in range(len(ct))).decode(errors='ignore')

        if "Cyberthon" in pt:
            flag = re.findall(r'(Cyberthon{.+?})', pt)[0].strip()

            print("Key:", key.hex())
            print("Flag:", flag)
            break