import hashlib
import re

msgs = [
    b'Beware the Krampus Syndicate!',
    b'Santa is watching...',
    b'Good luck getting the key'
]

sig_hex = []

with open("out.txt", "r") as f:
    lines = [line for line in f.read().split("msg") if len(line)]

    for line in lines:
        r = re.findall(r'r  :(.+)', line)[0].strip()
        s = re.findall(r's  :(.+)', line)[0].strip()

        sig_hex.append((r, s))

n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def inv_mod(k, p):
    return pow(k, p - 2, p)

r = []
s = []
z = []

for i in range(3):
    r_i = int(sig_hex[i][0], 16)
    s_i = int(sig_hex[i][1], 16)
    r.append(r_i)
    s.append(s_i)
        
    h = hashlib.sha256(msgs[i]).digest()
    z_i = int.from_bytes(h, 'big')
    z.append(z_i)

s1_inv = inv_mod(s[0], n)
s2_inv = inv_mod(s[1], n)

numerator = (1 + (s1_inv * z[0] % n) - (s2_inv * z[1] % n)) % n
denominator = ((s2_inv * r[1] % n) - (s1_inv * r[0] % n)) % n
denominator_inv = inv_mod(denominator, n)

d = (numerator * denominator_inv) % n
k_plus_2 = (inv_mod(s[2], n) * (z[2] + r[2] * d)) % n
k = (inv_mod(s[0], n) * (z[0] + r[0] * d)) % n

key_bytes = d.to_bytes(32, 'big')
print(f"\nFlag: {key_bytes.decode()}")