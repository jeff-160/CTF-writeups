import requests
import re

url = "http://chal.thjcc.org:14514/"

res = requests.post(url, params={
    'n': '777'
})

flag = re.findall(r'(THJCC{.+})', res.text)[0]
print("Flag:", flag)