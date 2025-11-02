## treasure hunt

Category: Web  
Difficulty: Hard

<img src="images/chall.png" width=400>

We are given a webpage where we can submit our name for a greeting message.  

<img src="images/webpage.png" width=500>

The greeting message hints that there is an SSTI vulnerability within the webpage.  

<img src="images/hint.png" width=500>

Running a simple Python SSTI payload shown below gave an error, which revealed that the server used Node.js Nunjucks for templating rather than Jinja.  

```python
{{ self.__init__.__globals__.__builtins__['__import__']('os') }}
```

<img src="images/error.png" width=800>

With this knowledge, we can craft a simple payload that gives us RCE on the webpage.  

```javascript
{{ range.constructor('return process')().mainModule.require('child_process').execSync('ls').toString() }}
```

Running `ls` then reveals the entire directory structure.  

<img src="images/files.png" width=400>

To spare you the details, we have to read `flags/part1.txt`, `flags/secret.bat`, `part2.txt` and `server.js` to retrieve and reassemble all parts of the flag.  

Flag: `GCTF25{5STI_p47H_7Rav3R5A1_M45teR}`
