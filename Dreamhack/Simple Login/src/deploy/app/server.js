const cookieParser = require('cookie-parser');
const crypto = require('crypto');
const express = require('express');
const fs = require('node:fs');
const jwt = require('jsonwebtoken');
const path = require('path');

const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(cookieParser());
app.use(express.urlencoded({ extended: true }));

const FLAG = readFile('/flag');

const privKey = readFile('/priv.pem');
const verificationKey = readFile('/pub.crt');

const accounts = {
    'admin': {
        'password': FLAG
    },
    'guest': {
        'password': 'guest'
    }
};
 
function readFile(filePath) {
    try {
        return fs.readFileSync(filePath, { encoding: 'utf8' });
    } catch (err) {
        console.error(err);
        process.exit(1);
    }
}

function verifyToken(token) {
    try {
        const alg = jwt.decode(token, { complete: true }).header.alg;
        if (alg === 'RS256') {
            return jwt.verify(token, verificationKey);
        } else if (alg === 'HS256') {
            return jwt.verify(token, verificationKey, { algorithms: ['HS256'] });
        } else if (alg === 'ES256') {
            return jwt.verify(token, verificationKey, { algorithms: ['ES256'] });
        } else {
            return false;
        }
    } catch (error) {
        return false;
    }
}

function createAccountToken(username) {
    const payload = {'username': username};
    const options = { expiresIn: '1h', algorithm: 'RS256' };  // We only support RS256 :)

    return jwt.sign(payload, privKey, options);
}

function isAdmin(token) {
    var decoded = verifyToken(token);

    if (decoded.username === 'admin') {
        return true;
    }
    return false;
}

function requireAuthentication(req, res, next) {
    if (typeof req.cookies.token !== 'string') {
        res.redirect('/login');
        return;
    }

    if (verifyToken(req.cookies.token) === false) {
        res.clearCookie('token').redirect('/login');
        return;
    }

    next();
}

function requireNoAuthentication(req, res, next) {
    if (typeof req.cookies.token === 'string') {
        res.status(403);
        res.send('you are already logged in.');
        return;
    }

    next();
}

app.get('/login', requireNoAuthentication, (req, res) => {
    res.render('login');
});

app.post('/login', requireNoAuthentication, (req, res) => {
    const username = req.body.username;
    const password = req.body.password;
    if (!username || !password) {
        res.status(400);
        res.send('username or password is empty.');
        return;
    }

    const passwordHash = crypto.createHash('sha256').update(password).digest('hex');
    if (!username in accounts) {
        res.status(401);
        res.send('username or password is wrong.');
        return;
    }

    const accountPasswordHash = crypto.createHash('sha256').update(accounts[username]['password']).digest('hex');
    if (!crypto.timingSafeEqual(Buffer.from(passwordHash),
                                Buffer.from(accountPasswordHash))) {
        res.status(401);
        res.send('username or password is wrong.');
        return;
    }

    res.cookie('token', createAccountToken(username), { httpOnly: true });
    res.redirect('/');
});

app.post('/logout', (req, res) => {
    res.clearCookie('token').redirect('login');
});

app.get('/admin', (req, res) => {
    if (isAdmin(req.cookies.token) !== true) {
        res.status(404);
        res.send('page not found.');
        return;
    }
    res.send(FLAG);
});

app.get('/', requireAuthentication, (req, res) => {
    res.render('index', { isAdmin: isAdmin(req.cookies.token) });
});

app.listen(7000, '0.0.0.0');
