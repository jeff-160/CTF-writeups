from secret import p, q
import os
from Crypto.Util.number import bytes_to_long, isPrime

assert isPrime(p) and p.bit_length() <= 512
assert isPrime(q) and q.bit_length() <= 512

with open('flag.txt', 'rb') as f:
    FLAG = f.read()

N = p * q

e1 = 65537
e2 = 65583

m = bytes_to_long(FLAG)
c = pow(m, e1, N)

c1 = pow(p + q, e2, N)

p = str(p)
q = str(q)
c2 = pow(int(p + q), e2, N)

print(f'{N = }')
print(f'{e1 = }')
print(f'{e2 = }')
print(f'{c = }')
print(f'{c1 = }')
print(f'{c2 = }')