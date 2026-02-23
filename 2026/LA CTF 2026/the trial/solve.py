import requests
import re

url = "https://the-trial.chall.lac.tf/"

res = requests.post(f'{url}/getflag', data={
    'word': 'flag'
}, headers={"Content-Type": "application/x-www-form-urlencoded"})

flag = re.findall(r'(lactf{.+})', res.text)[0]
print("Flag:", flag)