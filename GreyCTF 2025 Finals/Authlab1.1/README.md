## Authlab1.1

Category: Misc

i spent more than half a day on this lol 🥀

<img src="images/challenge.png" width=400>

We have the exact same setup as the previous challenge, however, the server uses a custom Pickle deserialiser to process our payload. 

<img src="images/vuln.png" width=400>

In `SecurePickle`, we can see that only module imports from `builtins` are allowed, and that it also checks our payload against a blacklist.  

As such, the standard Pickle `__reduce__` RCE exploit wouldn't suffice in this case.  

<img src="images/securepickle.png" width=600>

After some digging, I found a [github article](https://github.com/maurosoria/dirsearch/issues/1073) that detailed how to bypass a similar setup.  

The author linked his own [tool](https://github.com/splitline/Pickora) that converted Python to Pickle bytecode, which will allow us to bypass the `builtins` import filter (idk how it just works).  

We can dump the same payload as before into Pickle bytecode, however, we need to use some obfuscations to bypass the blacklist this time.

```bash
pickora -c "getattr(getattr(print.__self__, ''.join(['__imp', 'ort__']))(''.join(['o', 's'])), ''.join(['sy', 'stem']))(''.join(['s','h']))" -e
```

After entering our Base64 payload, we indeed get a shell where we can read the flag.  

<img src="images/flag.png" width=600>