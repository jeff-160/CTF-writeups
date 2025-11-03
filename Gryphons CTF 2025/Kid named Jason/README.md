## Kid named Jason

Category: Web  
Difficulty: Medium

<img src="images/chall.png" width=400>

The webpage we are provided with gives us some instructions.  

<img src="images/webpage.png" width=400>

Visiting the `/token` endpoint does indeed give us a sample token.  

<img src="images/token.png" width=600>

When we try visiting the `/verify` endpoint with our token we get this error.  

```
{"error":"The specified key is an asymmetric key or x509 certificate and should not be used as an HMAC secret.","file_leak":"-----BEGIN PUBLIC KEY-----\nFAKEPUBLICKEY\n-----END PUBLIC KEY-----\n","ok":false}
```

The first thing we may notice is that the error message has a `file_leak` parameter, and the contents of a public key file seem to be outputted.  

Decoding the JWT token from Base64 shows a `kid` parameter in the token header containing the path to a public key.  

<img src="images/jwt.png" width=500>

This points towards an LFI vulnerability. When we change `kid` to a known file like `/etc/passwd`, the server does indeed return the file's contents.  

<img src="images/lfi.png" width=600>

This means that if we are able to locate the flag file, we can get the server to output it and print out the flag.  

After some guesses, I found it in `/flag.txt`.  

<img src="images/flag.png" width=600>

Flag: `GCTF25{t0ken_of_4ppreciation}`
