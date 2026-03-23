from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime
from random import randint

def hkdf_mask(secret: bytes, length: int) -> bytes:
  hkdf = HKDF(
    algorithm=hashes.SHA256(),
    length=length,
    salt=None,
    info=b"rsa-d-mask",
    backend=default_backend()
  )
  return hkdf.derive(secret)

# RSA
q1 = getPrime(512)
q2 = getPrime(512)
n = q1 * q2
e = 65537
phi = (q1 - 1) * (q2 - 1)
d = pow(e, -1, phi)

# DLP
p = 200167626629249973590210748210664315551571227173732968065685194568612605520816305417784745648399324178485097581867501503778073506528170960879344249321872139638179291829086442429009723480288604047975360660822750743411854623254328369265079475034447044479229192540942687284442586906047953374527204596869578972378578818243592790149118451253249
g = 11
s = randint(1, 1 << 100)
A = pow(g, s, p)

D = d ^ bytes_to_long(hkdf_mask(long_to_bytes(s), d.bit_length() // 8))

with open('flag.txt', 'r') as outfile:
  flag = outfile.read()

c = pow(bytes_to_long(flag.encode()), 2, n)

print("---- RSA Public Data ----")
print(f"{n=}")
print(f"{e=}")
print("---- DLP Public Data ----")
print(f"{p=}")
print(f"{g=}")
print(f"{A=}")
print("---- Encrypted Data ----")
print(f"{D=}")
print(f"{c=}")
