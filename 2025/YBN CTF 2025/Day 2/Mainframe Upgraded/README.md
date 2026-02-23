## Mainframe Upgraded?

<img src="images/chall.png" width=600>

We are given an improved version of the webpage from the guided SSTI chall.  

<img src="images/webpage.png" width=600>

The challenge description hints at this still being an SSTI chall, and the message on the webpage hints at Node.js SSTI.  

We can test for SSTI with a simple Node.js template injection payload.  

<img src="images/ssti.png" width=600>

We can easily get RCE and inspect the directory structure with this payload.  

```js
<%- process.mainModule.require('child_process').execSync('ls') %>
```

<img src="images/ls.png" width=600>

We can read just read the flag file to get the flag. The characters of the flag are prepended with null bytes but you can just remove those with Python.  

<img src="images/flag.png" width=600>

Flag: `YBN25{santa_says_ssti_h0_h0_hacked}`