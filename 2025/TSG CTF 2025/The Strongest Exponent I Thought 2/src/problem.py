from Crypto.Util.number import getPrime

flag = "TSGCTF{************REDACTED*************}"
assert len(flag) == 41

p = getPrime(1024)
q = getPrime(1024)
n = p * q
phi = (p - 1) * (q - 1)
# e = (p ** q) % phi
e = pow(p, q, phi)

m = int.from_bytes(flag.encode(), 'big')

c = pow(m, e, n)

print(f"n = {n}")
print(f"e = {e}")
print(f"c = {c}")