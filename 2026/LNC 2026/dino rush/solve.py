import hmac
import hashlib
import json
import base64
import time
import requests

url = "http://chall1.lagncra.sh:18476/"

key = b"d1n0_s3cr3t_k3y_2403"
score = 9999

ts = int(time.time())
sig = hmac.new(key, f"{score}:{ts}".encode(), hashlib.sha256).hexdigest()

payload = {
    "score": score,
    "ts": ts,
    "sig": sig
}

token = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()

res = requests.post(f'{url}/api/submit', json={
    'token': token
})

print("Flag:", res.json()['flag'])