const express = require('express');
const path = require('path');
const app = express();
const port = 3000;
const _ = require('lodash');
const cookieParser = require('cookie-parser');
const crypto = require('crypto')

const DB = { default: "Default" };
const users = new Set();

const hashPasswd = p => { return crypto.createHash('sha256').update(p).digest('hex') };
let lastUserId = 0;

app.set('views', path.join(__dirname, '/templates'));
app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cookieParser());

app.get('/', (req, res) => {
   res.render('index', { db: JSON.stringify(DB) });
})

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

app.get('/api/get', (req, res) => {
   const { key } = req.query;
   const result = _.get(DB, key, false);
   if (result) res.json({ error: false, msg: result });
   else res.json({ error: true, msg: "failed" });
})

app.get('/api/set', (req, res) => {
   const { key, value } = req.query;
   _.set(DB, key, value);
   res.json({ error: false, msg: "success" });
})

app.get('/api/unset', (req, res) => {
   const { key } = req.query;
   const result = _.unset(DB, key);
   if (result) res.json({ error: false, msg: "success" });
   else res.json({ error: true, msg: "failed" });
})

app.post('/login', (req, res) => {
   const { username, password } = req.body;

   if (!username || !password)
      return res.json({ error: true, msg: "Enter username and password!" });

   let userInfo = null;
   for (let v of users.entries())
      if (v[0].username == username)
         userInfo = v[0];

   if (!userInfo)
      return res.json({ error: true, msg: "User not found!" });

   let hashedPassword = hashPasswd(password);
   if (userInfo.password != hashedPassword)
      return res.json({ error: true, msg: "User not found!" });

   res.cookie('uid', userInfo.uid);
   res.cookie('passwd', hashedPassword);
   res.json({ error: false, msg: "Log in success!" });
})

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

app.listen(port, () => { console.log("Server Running") })
users.add({ username: "admin", password: hashPasswd(crypto.randomBytes(64).toString('hex')), uid: lastUserId++ })
