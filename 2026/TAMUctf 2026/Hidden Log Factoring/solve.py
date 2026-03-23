"""
CTF Solve Script
================
Challenge structure:
  1. RSA keypair (n, e, d) — n is 1024-bit
  2. DLP: A = g^s mod p, with s < 2^100 (small secret)
  3. d is masked: D = d XOR HKDF(s)
  4. c = flag^2 mod n (Rabin encryption)

Attack chain:
  1. Pohlig-Hellman on the 2^101 subgroup of Z_p* → recover s
  2. Unmask d: d = D XOR HKDF(long_to_bytes(s), mask_len)
  3. Factor n using (e, d) via the standard Miller-Rabin trick
  4. Rabin decrypt: solve m^2 ≡ c (mod n) via CRT square roots
"""

import math
import random
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from Crypto.Util.number import long_to_bytes, bytes_to_long

# ── Given values ─────────────────────────────────────────────────────────────
n = 71016310005824589926747341243598522145452505235842335510488353587223142066921470760443852767377534776713566052988373656012584808377496091765373981120165220471527586994259252074709653090148780742972203779666231432769553199154214563039426087870098774883375566546770723222752131892953195949848583409407713489831
e = 65537

p = 200167626629249973590210748210664315551571227173732968065685194568612605520816305417784745648399324178485097581867501503778073506528170960879344249321872139638179291829086442429009723480288604047975360660822750743411854623254328369265079475034447044479229192540942687284442586906047953374527204596869578972378578818243592790149118451253249
g = 11
A = 44209577951808382329528773174800640982676772266062718570752782238450958062000992024007390942331777802579750741643234627722057238001117859851305258592175283446986950906322475842276682130684406699583969531658154117541036033175624316123630171940523312498410797292015306505441358652764718889371372744612329404629522344917215516711582956706994

D = 9478993126102369804166465392238441359765254122557022102787395039760473484373917895152043164556897759129379257347258713397227019255397523784552330568551257950882564054224108445256766524125007082113207841784651721510041313068567959041923601780557243220011462176445589034556139643023098611601440872439110251624
c = 1479919887254219636530919475050983663848182436330538045427636138917562865693442211774911655964940989306960131568709021476461747472930022641984797332621318327273825157712858569934666380955735263664889604798016194035704361047493027641699022507373990773216443687431071760958198437503246519811635672063448591496


# ── Step 1: Pohlig-Hellman DLP on 2^101 subgroup ────────────────────────────
# p-1 = 2^101 * 3 * 29 * 317 * 593 * 480661 * (large cofactor)
# Since s < 2^100, s is fully determined by s mod 2^101.
# We work in the unique subgroup of order 2^101 by raising g, A to the cofactor.

print("[*] Step 1: Pohlig-Hellman to recover s ...")

order_2 = 2 ** 101
cofactor = (p - 1) // order_2   # = 3 * 29 * 317 * 593 * 480661 * (large factor)

g2 = pow(g, cofactor, p)        # generator of the 2^101-order subgroup
A2 = pow(A, cofactor, p)        # A projected into that subgroup
g2_inv = pow(g2, -1, p)
g2_half = pow(g2, order_2 // 2, p)   # the unique element of order 2 in subgroup

# Recover bits of s one at a time (standard Pohlig-Hellman for prime power 2^k)
s = 0
cur = A2
for k in range(101):
    # Map current residual to the order-2 subgroup
    exp = order_2 >> (k + 1)
    lhs = pow(cur, exp, p)
    # lhs == 1  →  bit k of s is 0
    # lhs == g2^(2^100)  →  bit k of s is 1
    bit = 0 if lhs == 1 else 1
    s |= (bit << k)
    if bit:
        cur = cur * pow(g2_inv, 1 << k, p) % p

assert pow(g, s, p) == A, "DLP verification failed!"
print(f"[+] s = {s}  (bits: {s.bit_length()})")


# ── Step 2: Unmask d ─────────────────────────────────────────────────────────
# D = d XOR HKDF(long_to_bytes(s), d.bit_length() // 8)
# d ~ phi(n) ~ n (1024-bit), so d.bit_length() // 8 is 127 or 128.

print("[*] Step 2: Recovering d ...")

def hkdf_mask(secret: bytes, length: int) -> bytes:
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=length,
        salt=None,
        info=b"rsa-d-mask",
        backend=default_backend()
    )
    return hkdf.derive(secret)

s_bytes = long_to_bytes(s)
d = None
for mask_len in [127, 128]:
    mask = bytes_to_long(hkdf_mask(s_bytes, mask_len))
    d_cand = D ^ mask
    if d_cand < n:          # d must be < n for a valid RSA private key
        d = d_cand
        print(f"[+] d recovered (mask_len={mask_len}, bits={d.bit_length()})")
        break

assert d is not None, "Could not recover d!"


# ── Step 3: Factor n using (e, d) ────────────────────────────────────────────
# e*d ≡ 1 (mod phi(n))  →  e*d - 1 = 2^t * r
# For random a, compute a^r mod n and look for a non-trivial square root of 1.

print("[*] Step 3: Factoring n ...")

def factor_n_with_ed(n, e, d):
    k = e * d - 1          # k is a multiple of phi(n)
    t, r = 0, k
    while r % 2 == 0:
        r //= 2
        t += 1
    for _ in range(300):
        a = random.randint(2, n - 2)
        x = pow(a, r, n)
        if x in (1, n - 1):
            continue
        for _ in range(t - 1):
            y = pow(x, 2, n)
            if y == 1:
                f = math.gcd(x - 1, n)
                if 1 < f < n:
                    return f, n // f
            x = y
            if x == n - 1:
                break
    return None

result = factor_n_with_ed(n, e, d)
assert result, "Factoring failed!"
q1, q2 = result
assert q1 * q2 == n
print(f"[+] Factored n: q1 has {q1.bit_length()} bits, q2 has {q2.bit_length()} bits")


# ── Step 4: Rabin decryption (c = m^2 mod n) ─────────────────────────────────
# Compute square roots of c mod q1 and mod q2, then CRT-combine for 4 candidates.

print("[*] Step 4: Rabin decryption ...")

def tonelli_shanks(n, p):
    """Compute square root of n mod p (prime). Returns None if not a QR."""
    if pow(n, (p - 1) // 2, p) != 1:
        return None
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    # General Tonelli-Shanks
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m, c2, t, r = s, pow(z, q, p), pow(n, q, p), pow(n, (q + 1) // 2, p)
    while True:
        if t == 1:
            return r
        i, tmp = 1, pow(t, 2, p)
        while tmp != 1:
            tmp = pow(tmp, 2, p)
            i += 1
        b = pow(c2, 1 << (m - i - 1), p)
        m, c2, t, r = i, pow(b, 2, p), t * pow(b, 2, p) % p, r * b % p

def crt_combine(a, b, p, q):
    """CRT: find x with x≡a (mod p), x≡b (mod q), 0 ≤ x < p*q."""
    return (a + p * ((b - a) * pow(p, -1, q) % q)) % (p * q)

r1 = tonelli_shanks(c % q1, q1)
r2 = tonelli_shanks(c % q2, q2)
assert r1 and r2, "c is not a QR mod one of the factors!"

# 4 candidate plaintexts: (±r1 mod q1, ±r2 mod q2)
print("[+] Trying all 4 Rabin roots ...")
for s1 in [r1, q1 - r1]:
    for s2 in [r2, q2 - r2]:
        m = crt_combine(s1, s2, q1, q2)
        raw = long_to_bytes(m)

        if b'gigem' in raw:
            print("Flag:", raw.decode().strip())
            exit()