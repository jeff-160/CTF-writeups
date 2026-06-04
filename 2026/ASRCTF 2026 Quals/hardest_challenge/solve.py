KEY_FILE = "keys.txt"
CT_FILE  = "ciphertext.txt"

ct = open(CT_FILE, "rb").read()
LENGTH = len(ct)

# XOR is commutative and associative — order of keys doesn't matter.
# XOR all 676,767 keys together to get the combined key mask,
# then XOR that with the ciphertext to recover the flag.
combined = bytearray(LENGTH)
with open(KEY_FILE, "rb") as f:
    while chunk := f.read(LENGTH):
        if len(chunk) != LENGTH:
            break
        for i in range(LENGTH):
            combined[i] ^= chunk[i]

flag = bytes(ct[i] ^ combined[i] for i in range(LENGTH))
print(flag.decode())