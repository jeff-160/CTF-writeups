import requests
import base64
import re

DB = "https://bpmyujqesbysrbbqjdcb.supabase.co"

key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJwbXl1anFlc2J5c3JiYnFqZGNiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUyODcxODUsImV4cCI6MjA4MDg2MzE4NX0.xzmN7tAV9Tq0hLVp66uiIiWFk_dZlv92n0_V1qQXA0o'
headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
}

# mint john's token with exp
payload = b"|acc=private"
exp = '9' * (len(payload) + 1)

res = requests.post(f"{DB}/functions/v1/mint_token", headers=headers, json={ 
    'email': 'johndoe@ybn.sg',
    'exp': int(exp)
})

token = res.json()['token']
print("Token:", token)

# change public to private
cipher = bytearray(base64.b64decode(token))
BLOCK = 16
old = exp[:-1].encode()

for block in range(1, len(cipher) // BLOCK):
    for offset in range(BLOCK - len(old)):
        test = cipher[:]

        for i in range(len(old)):
            test[block * BLOCK - BLOCK + offset + i] ^= old[i] ^ payload[i]

        forged = base64.b64encode(test).decode()

        res = requests.post(f"{DB}/functions/v1/view_profile", headers=headers, json={"token": forged})

        try:
            flag = re.findall(r'(YBN25\{.+?\})', res.text)[0]
            print("Flag:", flag)
            exit()
        except:
            ...