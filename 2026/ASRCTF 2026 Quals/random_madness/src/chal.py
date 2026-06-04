import ast
import re
from sympy import nextprime
from Crypto.Util.number import long_to_bytes

# ---------------- MT19937 ---------------- #

class MT19937:
    def __init__(self):
        self.mt = [0]*624
        self.index = 624

    def untemper(self, y):
        y ^= y >> 18
        y ^= (y << 15) & 0xefc60000
        for _ in range(2):
            y ^= (y << 7) & 0x9d2c5680
        for _ in range(2):
            y ^= y >> 11
        return y & 0xffffffff

    def set_state(self, outputs):
        self.mt = [self.untemper(x) for x in outputs]
        self.index = 624

    def extract(self):
        if self.index >= 624:
            self.twist()
        y = self.mt[self.index]
        self.index += 1
        return y

    def twist(self):
        for i in range(624):
            y = (self.mt[i] & 0x80000000) + (self.mt[(i+1)%624] & 0x7fffffff)
            self.mt[i] = self.mt[(i+397)%624] ^ (y >> 1)
            if y & 1:
                self.mt[i] ^= 0x9908b0df
        self.index = 0


# ---------------- load file ---------------- #

data = open("dist.txt").read()

leak_str, plain = ast.literal_eval(data.split("leak = ")[1].split("\n")[0])

# 🔥 FIX: correct parsing of hex stream
cipher_vals = list(map(lambda x: int(x, 16), re.findall(r'0x[0-9a-fA-F]+', leak_str)))

# recover MT outputs
rng_outputs = [c ^ ord(p) for c, p in zip(cipher_vals, plain)]

assert len(rng_outputs) == 624

# ---------------- recover MT ---------------- #

mt = MT19937()
mt.set_state(rng_outputs)

# NO OFFSET GUESSING — trust correct state
x1 = mt.extract()
x2 = mt.extract()

p = nextprime(int(str(x1) * 10))
q = nextprime(int(str(x2) * 10))

# ---------------- RSA ---------------- #

n = int(data.split("n = ")[1].split("\n")[0])
enc = int(data.split("enc = ")[1].split("\n")[0])

phi = (p - 1) * (q - 1)
d = pow(65537, -1, phi)

m = pow(enc, d, n)

print(long_to_bytes(m))