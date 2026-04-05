import requests

url = "https://heap.vishwactf.com/"

res = requests.get(f'{url}/api/init')

data = res.json()
key, decoded = data['session_seed'], data['trace_vector']

decoded = [i ^ key for i in decoded]
token = ''.join(chr(c) for c in decoded)

print("Flag:", token)