'use strict'

const express = require('express')
const { VM } = require('vm2')

const app = express()
const PORT = 9797

app.use(express.json({ limit: '64kb' }))

const INDEX_HTML = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Jelly Box</title>
<style>
    body {
        background: #1a0f1f;
        color: #ffe0f5;
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        margin: 0;
        padding: 40px;
        display: flex;
        justify-content: center;
    }
    .wrap { max-width: 760px; width: 100%; }
    h1 {
        font-size: 32px;
        margin: 0 0 4px;
        color: #ff77c8;
        text-shadow: 0 0 12px rgba(255, 119, 200, 0.45);
    }
    .sub { color: #b48fb8; margin-bottom: 24px; font-size: 13px; }
    textarea {
        width: 100%;
        height: 220px;
        background: #2a1632;
        color: #ffe0f5;
        border: 1px solid #5a2b6a;
        border-radius: 10px;
        padding: 14px;
        font-family: inherit;
        font-size: 13px;
        box-sizing: border-box;
        outline: none;
    }
    textarea:focus { border-color: #ff77c8; }
    button {
        background: #ff77c8;
        color: #1a0f1f;
        border: 0;
        padding: 10px 22px;
        font-weight: 700;
        border-radius: 999px;
        cursor: pointer;
        margin-top: 12px;
        font-family: inherit;
    }
    button:hover { background: #ffa3da; }
    pre {
        background: #2a1632;
        border: 1px solid #5a2b6a;
        border-radius: 10px;
        padding: 14px;
        white-space: pre-wrap;
        word-break: break-all;
        min-height: 60px;
        color: #ffe0f5;
    }
    h3 { color: #ff77c8; margin-top: 24px; }
</style>
</head>
<body>
<div class="wrap">
    <h1>Jelly Box</h1>
    <textarea id="code" spellcheck="false" placeholder="// your code here"></textarea>
    <br>
    <button onclick="run()">run</button>
    <h3>output</h3>
    <pre id="out"></pre>
</div>
<script>
async function run() {
    const code = document.getElementById('code').value
    const out = document.getElementById('out')
    out.textContent = '...'
    try {
        const r = await fetch('/run', {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({ code })
        })
        const j = await r.json()
        out.textContent = JSON.stringify(j, null, 2)
    } catch (e) {
        out.textContent = String(e)
    }
}
</script>
</body>
</html>`

app.get('/', (req, res) => {
    res.type('html').send(INDEX_HTML.replace('__NODEV__', process.versions.node))
})

app.post('/run', (req, res) => {
    const code = (req.body && typeof req.body.code === 'string') ? req.body.code : ''
    if (!code) {
        return res.status(400).json({ ok: false, error: 'missing code' })
    }
    if (code.length > 235) {
        return res.status(413).json({ ok: false, error: 'payload too large' })
    }

    const vm = new VM({
        timeout: 2000
    })

    try {
        const result = vm.run(code)
        let out
        try { out = String(result) } catch { out = '[unserializable]' }
        res.json({ ok: true, result: out })
    } catch (e) {
        res.json({ ok: false, error: String(e && e.stack || e) })
    }
})

app.listen(PORT, '0.0.0.0', () => {
    console.log(`[jelly-box] listening on http://0.0.0.0:${PORT}`)
})