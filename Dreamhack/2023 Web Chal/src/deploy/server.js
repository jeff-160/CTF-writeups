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
