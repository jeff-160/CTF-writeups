const express = require('express')
const jwt = require('jsonwebtoken');
const fs = require('fs')
const sshpk = require('sshpk');
const cookieParser = require('cookie-parser')

const app = express()

app.set("view engine", "ejs");
app.use(express.json());
app.use(cookieParser())

const PRIVATE_KEY = fs.readFileSync('private').toString()
const PUBLIC_KEY = fs.readFileSync('public.pub').toString()

const default_theme = {
    dark: {
        colors: {
            background: "#121212",
            text: "#ffffff",
        }
    },
    light: {
        colors: {
            background: "#ffffff",
            text: "#121212",
        }
    }
};

let users = {
    admin: "REDACTED"
}

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

const parseKey = (keytype, Key, options = {}) => {
    let key
    if (keytype === "private") {
        key = sshpk.parsePrivateKey(Key, 'ssh');
    } else {
        key = sshpk.parseKey(Key, 'ssh', { filename: "publickey" });
    }
    return key.toString(options.format || 'pkcs8')
}

app.get('/login', (req, res) => {
    res.render('login');
});

app.get('/', (req, res) => {
    let user = ""
    try {
        const token = req.cookies["token"]
        const decoded = jwt.verify(token, parseKey("public", PUBLIC_KEY));
        user = decoded.user
    } catch (e) {
        user = ""
    }
    res.render('dashboard', { user: user });
});

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

//api codes

app.post('/api/theme', (req, res) => {
    const { base, customizations } = req.body;
    try {
        const theme = ThemeManager.createTheme(base, customizations);
        res.json({ success: true, theme: theme });
    } catch (err) {
        res.status(400).json({ error: 'invalid theme' });
    }
});

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

app.listen(8000, () => {
    console.log('running on port 8000');
});