from Crypto.Util.strxor import strxor

ct_hex = "9f2eadbd998e9ca1aab6bfbba9bf85afa9bf85a9bfb9a8bfaea985b3b485a3b5afa885a9aea8bfbbb785b9b3aab2bfa8a985ece3b8bcbfebe3eebbbceee9bceab9bea7"
ct = bytes.fromhex(ct_hex)

def gen(start):
    return (((6 * 7) * (start - 6) * 7) + ((start * 6) - 7) * (start ^ 6)) % 255

def build_key(start, length):
    key = [start]
    for i in range(1, length):
        key.append(gen(key[i-1]))
    return bytes(key)

for start in range(256):
    key = build_key(start, len(ct))
    pt = strxor(key, ct)

    if pt.startswith(b"DawgCTF{"):
        print("start =", start)
        print("flag =", pt.decode(errors="ignore"))
        break