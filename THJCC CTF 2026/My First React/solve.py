import time
import hashlib
import requests

url = "https://chal.thjcc.org:25600"

bucket = int(time.time() * 1000 // 10000)
hash = hashlib.sha1(str(bucket).encode()).hexdigest()

res = requests.get(f"{url}/{hash}")
print("Flag:", res.json()['result'])