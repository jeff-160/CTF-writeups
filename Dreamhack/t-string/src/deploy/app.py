from flask import Flask, request, g, session, redirect
from string.templatelib import Template, Interpolation
from datetime import datetime
import os
import sqlite3
import re

app = Flask(__name__)
app.secret_key = os.urandom(32)

DATABASE = "database.db"

def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)
    db.execute(f"INSERT INTO users(username, password) VALUES ('admin', '{os.urandom(16).hex()}')")
    db.commit()
    db.close()

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def sql_safe(func: callable):
    parts = []
    def wrapper(query: Template):
        parts.clear()
        for i in query:
            match i:
                case str() as s:
                    parts.append(s)
                case Interpolation(value, expression, conversion, format_spec):
                    value = str(value)
                    value = re.sub(r"'", "''", value)
                    value = re.sub(r"SELECT|UNION|INSERT|UPDATE|DELETE", "", value, flags=re.IGNORECASE)
                    parts.append(value)

        query = "".join(parts)
        return func(query)

    return wrapper

@sql_safe
def select_one(query: Template):
    db = get_db()
    cur = db.execute(query)
    row = cur.fetchone()
    cur.close()
    return row

@sql_safe
def insert(query: Template):
    db = get_db()
    cur = db.execute(query)
    db.commit()
    last_id = cur.lastrowid
    cur.close()
    return last_id


def escape(s: str):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&#34;").replace("'", "&#39;")

def get_attr_safe(obj, attr):
    for keyword in ["class", "global", "builtins", "get", "mro", "module", "import", "eval", "exec"]:
        if keyword in attr:
            return ""
    try:
        return str(eval(f"obj['{attr}']", {"__builtins__": {}}, {"obj": obj}))
    except:
        try:
            return str(eval(f"obj.{attr}", {"__builtins__": {}}, {"obj": obj}))
        except:
            return ""

def render_template(template: Template):
    parts = []
    for i in template:
        match i:
            case str() as s:
                parts.append(s)
            case Interpolation(value, expression, conversion, format_spec):
                match format_spec:
                    case "safe":
                        value = str(value)
                    case "xmlattr":
                        value = " ".join(f'{escape(str(k))}="{escape(str(v))}"' for k, v in value.items())
                    case str() if (m := re.match(r'attr\((.*)\)', format_spec)):
                        value = escape(get_attr_safe(value, m.group(1)))
                    case _:
                        value = escape(format(value, format_spec))
                
                parts.append(value)
    return "".join(parts)



@app.route("/", methods=["GET"])
def index():
    if session.get("username") is None:
        return redirect("/login")
    
    name = session.get("username")
    color = request.args.get("color", "black")
    tag_attr = {
        "style": f"color: {color};",
        "class": "greeting",
    }
    greeting_map = {"ko" : "안녕하세요", "en": "Hello", "jp": "こんにちは"}
    lang = request.args.get("lang", "ko")
    lang = "ko" if lang not in greeting_map else lang

    template = t'<h1 {tag_attr:xmlattr}>{greeting_map:attr({lang})}, {name}!</h1>'

    return render_template(template)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return '''
        <form method="POST">
            Username: <input name="username" /><br/>
            Password: <input name="password" type="password" /><br/>
            <input type="submit" value="Login" />
        </form>
        '''
    else:
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        template = t"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        user = select_one(template)
        if user:
            session['username'] = user['username']
            return redirect("/")
        return '<script>alert("Invalid credentials");history.go(-1);</script>'

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return '''
        <form method="POST">
            Username: <input name="username" /><br/>
            Password: <input name="password" type="password" /><br/>
            <input type="submit" value="Register" />
        </form>
        '''
    else:
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        template = t"INSERT INTO users(username, password) VALUES ('{username}', '{password}')"
        try:
            insert(template)
            return '<script>alert("Registered successfully");location.href="/login";</script>'
        except sqlite3.IntegrityError:
            return '<script>alert("Username already exists");history.go(-1);</script>'
        
@app.route("/admin/server-time", methods=["GET"])
def server_time():
    if session.get("username") != "admin":
        return redirect("/login")

    time_fmt = request.args.get("time-fmt", "%Y-%m-%d %H:%M:%S")
    return render_template(t'Server time is: {datetime.now():{time_fmt}}')

if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        init_db()
    
    app.run('0.0.0.0', port=3000)