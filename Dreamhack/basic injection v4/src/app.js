const doT = require('dot');
const express = require('express');
const session = require('express-session');
const redis = require('redis');
const connectRedis = require('connect-redis');
const qs = require('qs');

const app = express();

app.set('query parser', function(str) {
    return qs.parse(str);
});
const redis_client = redis.createClient();

const RedisStore = connectRedis(session);
const sess = {
    resave: false,
    saveUninitialized: false,
    secret: '[REDACTED]',
    store: new RedisStore({
        client: redis_client
    }),
    cookie: {
        httpOnly: true,
        maxAge: null
    }
};

app.use(session(sess));

const db = {
    'guest': 'guest',
    'byte256': '[REDACTED]',
    'ADMIN': '[REDACTED]'
};

app.get('/', (req, res) => {
    const templateFn = doT.template(`<h1>Hello Guest</h1>`);
    res.send(templateFn({})); 
});

app.get('/login', function(req, res) {
    const userid = req.query.userid;
    const userpw = req.query.userpw;
    
    if (!userid || !userpw) {
        res.send('nope! ヾ (✿＞﹏ ⊙〃)ノ');
        return;
    }
    
    if (db[userid] && db[userid] === userpw) {
        req.session.userid = userid;
        res.send('ok');
    } else {
        res.send('nope! ヾ (✿＞﹏ ⊙〃)ノ');
    }
});

app.get('/option', function(req, res) {
    if (req.session.userid !== "admin") {
        res.send('nope! ヾ (✿＞﹏ ⊙〃)ノ');
        return;
    }
    
    const name = req.query.name || 'Admin';
    const templateFn = doT.template(`<h1>Hello ${name}</h1>`);
    res.send(templateFn({}));
});

app.get('/setting', function(req, res) {
    var log_query = req.query.log_query;
    
    try {
        log_query = log_query.split('/');
        if (log_query[0].toLowerCase() != 'get') {
            log_query[0] = 'get';
        }
        log_query[1] = log_query.slice(1);
    } catch (err) {
    }
    
    try {
        redis_client.send_command(log_query[0], log_query[1], function(err, result) {
            if (err) {
                res.send('nope! ヾ (✿＞﹏ ⊙〃)ノ');
            } else {
                res.send(result);
            }
        });
    } catch (err) {
        res.send('nope! ヾ (✿＞﹏ ⊙〃)ノ');
    }
});

app.listen(5000, () => console.log('Server is running!')); 