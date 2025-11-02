## Pantone

Category: Web  
Difficulty: Hard

<img src="images/chall.png" width=400>

We are given a webpage where we can mix colors.  

<img src="images/webpage.png" width=400>

In the source code, the flag is stored as a global variable.  

<img src="images/source_flag.png" width=500>

We can also notice that there's a prototype pollution vulnerability in one of the functions.  

<img src="images/vuln.png" width=500>

In the `/colors` endpoint, there's an `eval()` call which we can potentially hijack to get RCE.  

<img src="images/colors.png" width=400>

We can easily craft a payload that will cause the vulnerable function to recursively traverse to the global scope, where we can then overwrite `_EXEC_CMD` to `flag`.  

<img src="images/payload.png" width=400>

Sending the payload to the `/colors` endpoint will then cause the server to output the flag.  

Flag: `GCTF25{COL0Rfu1_C!a55_polLU71ON}`
