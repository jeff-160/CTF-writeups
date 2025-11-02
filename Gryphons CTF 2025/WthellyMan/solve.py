from itertools import product

m = 194408
pub = [1181,132565,52878,14172,46629,109833,77905,119928,125091,59050,29982,166439,160340,2362,81351,28344]
cipher = [25752,10517,177674,3616,85218,62159,50896,160827,82467,118388,66270,71879,18955,44216,142164,87189]

def solve_block(c):
    for bits in product([0,1], repeat=16):
        s = sum(pub[i]*bits[i] for i in range(16)) % m
        if s == c:
            return bits
    return None

plaintext_bits = []
for c in cipher:
    b = solve_block(c)
    if b is None:
        print("Failed for", c)
    else:
        plaintext_bits.extend(b)

plaintext = ''
for i in range(0, len(plaintext_bits), 8):
    byte = 0
    for j in range(8):
        byte = (byte << 1) | plaintext_bits[i+j]
    plaintext += chr(byte)
print(plaintext)
