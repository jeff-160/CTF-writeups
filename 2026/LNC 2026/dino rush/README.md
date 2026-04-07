## Dino Rush

<img src="images/chall.png" width=600>

This challenge involves a webpage where we can play the Chrome dinosaur game.  

We are required to farm `9999` points to get the website to generate a token, which can be used to claim the flag.  

<img src="images/website.png" width=600>

Inside the HTML source, we can find the `submitToken()` function, which makes a request to `/api/submit` with the specially crafted token to retrieve the flag.  

```js
async function submitToken() {
  const token = document.getElementById('token-input').value.trim();
  if (!token) { showResult('error', 'No token provided.'); return; }
  try {
    const res = await fetch('/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token })
    });
    const data = await res.json();
    if (data.success) showResult('success', `${data.message}\n\n🚩 ${data.flag}`);
    else showResult('error', data.error || 'Unknown error.');
  } catch(e) {
    showResult('error', 'Request failed: ' + e.message);
  }
}
```

We can also find a reference to `game.js` which contains the source code for the main game logic.  

<img src="images/game.png" width=600>

Inside, we can find the exact function being used to generate the token. `buildScoreToken()` crafts a token using the score, timestamp and signature.  

The signature is generated using the `_hmac()` function, which signs the message in the format `<score>:<timestamp>` using SHA-256. The signing is done with a secret key `_cfg._k`.  

```js
async function _hmac(key, message) {
    const enc = new TextEncoder();
    const cryptoKey = await crypto.subtle.importKey(
        "raw", enc.encode(key), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
    );
    const sig = await crypto.subtle.sign("HMAC", cryptoKey, enc.encode(message));
    return Array.from(new Uint8Array(sig)).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function buildScoreToken(score) {
    const ts = Math.floor(Date.now() / 1000);
    const sig = await _hmac(_cfg._k, `${score}:${ts}`);
    const payload = JSON.stringify({ score, ts, sig });
    return btoa(payload).replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
}
```

We can find `_cfg._k` declared above, with some slight obfuscations. Deobfuscating it gives `d1n0_s3cr3t_k3y_2403` as the secret key.  

```js
const _cfg = (function() {
    const _d = ["_s3c","2403","d1n0","k3y_","r3t_"];
    const _k = [_d[2], _d[0], _d[4], _d[3], _d[1]].join('');
    const _s = { threshold: 0x270F, version: "2.3.1" };
    return { _k, _s };
})();
```

Now that we know how the token generation works, we can reproduce it in Python and craft a token with the `score` field set to `9999`.  

Submitting the token to `/api/submit` will then give us the flag.  

```python
import hmac
import hashlib
import json
import base64
import time
import requests

url = "http://chall1.lagncra.sh:18476/"

key = b"d1n0_s3cr3t_k3y_2403"
score = 9999

ts = int(time.time())
sig = hmac.new(key, f"{score}:{ts}".encode(), hashlib.sha256).hexdigest()

payload = {
    "score": score,
    "ts": ts,
    "sig": sig
}

token = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()

res = requests.post(f'{url}/api/submit', json={
    'token': token
})

print("Flag:", res.json()['flag'])
```

Flag: `LNC26{3xt1nCt_but_n0t_f0rG0tT3n}`