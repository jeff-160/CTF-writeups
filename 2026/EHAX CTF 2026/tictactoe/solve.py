import requests

url = "https://ctf-challenge-1-beige.vercel.app/"

res = requests.post(f'{url}/api', json={
    'mode': '4x4',
    'state': [
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ]
})

print("Flag:", res.json()["flag"])