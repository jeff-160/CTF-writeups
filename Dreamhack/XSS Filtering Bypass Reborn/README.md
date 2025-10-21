## XSS Filtering Bypass Reborn

<img src="images/chall.png" width=400>

We are given a webpage that has a `/vuln` endpoint with an XSS vulnerability, as well as a `/flag` endpoint that will visit the vulnerable endpoint with a headless browser.  

<img src="images/source.png" width=500>

In the `/vuln` endpoint, our payload is already being put into an image that will auto trigger our payload, so our job is already being made slightly easier.  

<img src="images/vuln.png" width=400>

The base payload would be to redirect the headless browser (with the flag cookie) to the `/memo` endpoint and log the flag.  

I encoded the `"?"` beforehand so that the transpiler wouldn't hardcode it later on.  

```js
location.href='/memo\x3Fmemo='+document.cookie
```

Looking at the source code, we can see that our payload is being checked against a character blacklist, and this severely restricts our options.  

<img src="images/filter.png" width=500>

Thankfully, we can convert our payload to JSFuck to bypass most of the filter. I used https://js.retn0.kr/ in this case since the payloads generated are relatively shorter than other transpilers.  

<img src="images/jsfuck.png" width=600>

However, we still notice that the obfuscated payload still contains `"!"`, which violates the blacklist.  

The exclamation marks are mostly used to type-cast `[]` to booleans, and a similar effect can be achieved without them.  

```js
(+[]==+[])    // !![] or true

([]==[])      // ![] or false
```

I wrote a Python script to rewrite the payload as such, and submitting the payload in the `/flag` endpoint will then display the flag.  

<img src="images/flag.png" width=600>