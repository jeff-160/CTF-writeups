const express = require('express');
const cookieParser = require('cookie-parser');
const { NodeVM } = require('vm2');
const jwt = require('jsonwebtoken');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

const INITIAL_BALANCE = 100;
const MAX_BALANCE = 2000000;

const FLAG_PRICE = 1000000;
const FLAG_PATH = path.join(__dirname, 'flag.txt');

let FLAG = 'FLAG_NOT_FOUND';
try {
  FLAG = fs.readFileSync(FLAG_PATH, 'utf8').trim();
} catch (e) {
  console.error('[!] flag.txt 읽기 실패:', e);
}

const JWT_PRIVATE_KEY = fs.readFileSync(path.join(__dirname, 'jwtRS256.key'));
const JWT_PUBLIC_KEY = fs.readFileSync(path.join(__dirname, 'jwtRS256.key.pub'));
const JWT_PUBLIC_KEY_PEM = fs.readFileSync(path.join(__dirname, 'jwtRS256.key.pub'), 'utf8');

app.use(express.json());
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'html')));

function signUser(uid, role) {
  const payload = { uid, role };
  return jwt.sign(payload, JWT_PRIVATE_KEY, {
    algorithm: 'RS256',
    expiresIn: '1h'
  });
}

function getUserFromReq(req) {
  let token = req.cookies.auth;
  if (!token && req.headers.authorization && req.headers.authorization.startsWith('Bearer ')) {
    token = req.headers.authorization.slice(7);
  }
  if (!token) return null;

  try {
    const [headerB64] = token.split('.');
    const headerJson = Buffer.from(headerB64, 'base64url').toString('utf8');
    const header = JSON.parse(headerJson);

    let decoded;
    if (header.alg === 'RS256') {
      decoded = jwt.verify(token, JWT_PUBLIC_KEY, { algorithms: ['RS256'] });
    } else if (header.alg === 'HS256') {
      decoded = jwt.verify(token, JWT_PUBLIC_KEY_PEM, { algorithms: ['HS256'] });
    } else {
      throw new Error('unsupported alg');
    }

    return decoded;
  } catch (e) {
    return null;
  }
}

function requireAuth(req, res, next) {
  const user = getUserFromReq(req);
  if (!user) {
    return res.status(401).json({ error: '인증 필요' });
  }
  req.user = user;
  next();
}

function requireRole(role) {
  return (req, res, next) => {
    const user = getUserFromReq(req);
    if (!user) {
      return res.status(401).json({ error: '인증 필요' });
    }
    if (user.role !== role) {
      return res.status(403).json({ error: '권한 부족' });
    }
    req.user = user;
    next();
  };
}

const balances = new Map();

function getUserId(req) {
  const user = getUserFromReq(req);
  return user ? user.uid : 'guest';
}

function getBalance(req) {
  const uid = getUserId(req);
  let bal = balances.get(uid);
  if (bal === undefined) {
    bal = INITIAL_BALANCE;
    balances.set(uid, bal);
  }
  if (bal < -99999) bal = -99999;
  if (bal > MAX_BALANCE) bal = MAX_BALANCE;
  return bal;
}

function setBalance(req, balance) {
  const uid = getUserId(req);
  let bal = balance;
  if (bal < -99999) bal = -99999;
  if (bal > MAX_BALANCE) bal = MAX_BALANCE;
  balances.set(uid, bal);
}

app.post('/api/login/guest', (req, res) => {
  const uid = 'guest-' + Date.now().toString(36);
  const token = signUser(uid, 'user');
  res.cookie('auth', token, {
    httpOnly: true,
    sameSite: 'lax'
  });
  res.json({
    token,
    user: { uid, role: 'user' }
  });
});

app.get('/api/me', (req, res) => {
  const user = getUserFromReq(req);
  res.json({ user: user || null });
});

app.get('/api/balance', (req, res) => {
  res.json({ balance: getBalance(req) });
});

app.post('/api/spin', (req, res) => {
  const bet = parseInt((req.body && req.body.bet) || 0, 10);
  let bal = getBalance(req);

  if (!Number.isFinite(bet) || bet <= 0) {
    return res.status(400).json({ error: 'invalid bet' });
  }
  if (bet > bal) {
    return res.status(400).json({ error: '잔액 부족' });
  }

  const symbols = ['🍒', '🍋', '⭐', '7'];
  const reels = [
    symbols[Math.floor(Math.random() * symbols.length)],
    symbols[Math.floor(Math.random() * symbols.length)],
    symbols[Math.floor(Math.random() * symbols.length)]
  ];

  let delta;
  let message;
  if (reels[0] === '7' && reels[1] === '7' && reels[2] === '7') {
    delta = 100;
    message = 'JACKPOT! +100 크레딧!';
  } else if (reels[0] === reels[1] && reels[1] === reels[2]) {
    delta = 30;
    message = '트리플 매치! +30 크레딧!';
  } else {
    delta = -bet;
    message = `꽝… -${bet} 크레딧.`;
  }

  bal += delta;
  setBalance(req, bal);

  res.json({
    reels,
    delta,
    balance: bal,
    message
  });
});

app.post('/api/strategy/run', requireRole('vip'), (req, res) => {
  const code = (req.body && req.body.code) ? String(req.body.code) : '';

  if (!code || code.length > 4000) {
    return res.status(400).json({ error: 'invalid code length' });
  }
  const blackList = /\brequire\b|\bprocess\b|\bchild_process\b|\bfs\b/;
  if (blackList.test(code)) {
    return res.status(400).json({ error: 'forbidden identifier in code' });
  }

  const logs = [];
  const sandbox = {
    balance: getBalance(req),
    history: [],
    spin: (bet) => {
      let bal = sandbox.balance;
      bet = parseInt(bet, 10) || 0;
      if (bet <= 0) {
        return { error: 'invalid bet' };
      }
      if (bet > bal) {
        return { error: '잔액 부족' };
      }

      const symbols = ['🍒', '🍋', '⭐', '7'];
      const reels = [
        symbols[Math.floor(Math.random() * symbols.length)],
        symbols[Math.floor(Math.random() * symbols.length)],
        symbols[Math.floor(Math.random() * symbols.length)]
      ];

      let delta;
      if (reels[0] === '7' && reels[1] === '7' && reels[2] === '7') {
        delta = 100;
      } else if (reels[0] === reels[1] && reels[1] === reels[2]) {
        delta = 30;
      } else {
        delta = -bet;
      }

      bal += delta;
      sandbox.balance = bal;
      const info = { bet, reels, delta, balance: bal };
      sandbox.history.push(info);
      return info;
    }
  };

  const vm = new NodeVM({
    console: 'redirect',
    sandbox: { sandbox },
    timeout: 1000,
    eval: false,
    wasm: false
  });

  vm.on('console.log', (msg) => {
    logs.push(String(msg));
  });

  let result;
  try {
    result = vm.run(code, 'strategy.js');
  } catch (e) {
    return res.status(400).json({ error: String(e), logs });
  }

  setBalance(req, sandbox.balance);

  return res.json({
    result: result === undefined ? null : result,
    logs,
    finalBalance: sandbox.balance,
    spins: sandbox.history
  });
});

app.post('/api/shop/flag', (req, res) => {
  let bal = getBalance(req);

  if (bal < FLAG_PRICE) {
    return res.status(400).json({
      error: `잔액이 부족합니다. 플래그 가격은 ${FLAG_PRICE} 크레딧입니다.`,
      balance: bal
    });
  }

  bal -= FLAG_PRICE;
  setBalance(req, bal);

  return res.json({
    message: '플래그를 구매했습니다.',
    flag: FLAG,
    balance: bal
  });
});

app.get('/helpsign', (req, res) => {
  res.type('text/plain');
  res.sendFile(path.join(__dirname, 'jwtRS256.key.pub'));
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'html', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`[*] VM-JWT Casino listening on http://0.0.0.0:${PORT}`);
});
