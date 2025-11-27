def get_hex(raw):
    enc = []
    i = 0
    
    while i < len(raw):
        if raw[i] == "\\":
            enc.append(raw[i + 1 : i + 1 + 2])
            i += 3
        else:
            enc.append(format(ord(raw[i]), '02x'))
            i += 1
    
    return enc

enc = bytes.fromhex(''.join(get_hex(r"\9dn\93\c8\b2\b9A\8b\9f\90\8cb\c5\c3\95\884\c8\93\92\88?\c1\92\c7\db?\c8\9e\c7\891\c6\c5\c9\8b6\c6\c6\c0\90\00\00")))
key = [int(b, 16) for b in get_hex(r"\f1\a7\f0\07\ed")]

out = []
for i in range(len(enc)):
    k = key[4 - (i % 5)]
    out.append(enc[i] ^ k)

print(bytes(out).decode('utf-8', errors='ignore'))