import crypto from 'node:crypto'
import fs from 'node:fs'
import express from 'express'
import bcrypt from 'bcryptjs'
import multer from 'multer'
import tar from 'tar'
import mysql from 'mysql2/promise'
import { drizzle } from 'drizzle-orm/mysql2'
import { migrate } from 'drizzle-orm/mysql2/migrator'
import { sql } from 'drizzle-orm'

const PORT = Number(process.env.PORT ?? 3000)
const RELEASES_FOLDER = '/srv/releases'
const UPLOAD_TMP = '/srv/uploads'

if (!fs.existsSync(`${RELEASES_FOLDER}/meta/_journal.json`)) {
    fs.mkdirSync(`${RELEASES_FOLDER}/meta`, { recursive: true })
    fs.cpSync('./seed', RELEASES_FOLDER, { recursive: true })
}
fs.mkdirSync(UPLOAD_TMP, { recursive: true })

const conn = await mysql.createConnection({
    host: process.env.MYSQL_HOST,
    port: Number(process.env.MYSQL_PORT ?? 3306),
    user: process.env.MYSQL_USER,
    password: process.env.MYSQL_PASSWORD,
    database: process.env.MYSQL_DATABASE,
    multipleStatements: true,
})
const db = drizzle(conn)

function genToken() {
    return crypto.randomBytes(24).toString('hex')
}

async function authAccount(req) {
    const header = req.headers.authorization
    if (!header || !header.startsWith('Bearer ')) return null
    const token = header.slice(7).trim()
    if (!token) return null
    const [rows] = await conn.query(
        `SELECT a.id, a.email, a.role
           FROM sessions s
           JOIN accounts a ON a.id = s.account_id
          WHERE s.token = ? AND s.expires_at > NOW()
          LIMIT 1`,
        [token]
    )
    return rows[0] ?? null
}

async function requireAuth(req, res, next) {
    const account = await authAccount(req)
    if (!account) return res.status(401).json({ error: 'auth required' })
    req.account = account
    next()
}

async function requireOperator(req, res, next) {
    const account = await authAccount(req)
    if (!account || account.role !== 'operator') {
        return res.status(401).json({ error: 'operator auth required' })
    }
    req.account = account
    next()
}

const upload = multer({
    dest: UPLOAD_TMP,
    limits: { fileSize: 1 * 1024 * 1024 },
})

const app = express()
app.use(express.json({ limit: '32kb' }))

app.get('/', (_req, res) => {
    res.json({
        service: 'forecast',
        public: ['POST /signup', 'POST /login', 'GET /me', 'POST /reports/run'],
        admin:  ['POST /admin/upload-release', 'POST /admin/deploy-release'],
    })
})

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

app.post('/login', async (req, res) => {
    const { email, password } = req.body ?? {}
    if (typeof email !== 'string' || typeof password !== 'string') {
        return res.status(400).json({ error: 'email and password required' })
    }
    const [rows] = await conn.query(
        'SELECT id, password_hash, role FROM accounts WHERE email = ? LIMIT 1',
        [email]
    )
    const account = rows[0]
    if (!account) return res.status(401).json({ error: 'invalid credentials' })
    const ok = await bcrypt.compare(password, account.password_hash)
    if (!ok) return res.status(401).json({ error: 'invalid credentials' })

    const token = genToken()
    await conn.query(
        'INSERT INTO sessions (token, account_id, expires_at) VALUES (?, ?, NOW() + INTERVAL 1 DAY)',
        [token, account.id]
    )
    res.json({ token, role: account.role })
})

app.get('/me', requireAuth, async (req, res) => {
    res.json({ id: req.account.id, email: req.account.email, role: req.account.role })
})

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

app.listen(PORT, () => {
    console.log(`forecast listening on :${PORT}`)
})
