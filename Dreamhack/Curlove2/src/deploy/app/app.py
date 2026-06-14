import sqlite3
from os import urandom
from hashlib import md5
from utils import build_url
from ipaddress import ip_address
from subprocess import run,TimeoutExpired
from flask import Flask, request, g, render_template, session, redirect, abort

app = Flask(__name__)
app.secret_key = urandom(32)

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_user(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_user(query, args=()):
    db = get_db()
    cur = db.cursor()
    cur.execute(query, args)
    db.commit()
    rowcount = cur.rowcount
    cur.close()
    return rowcount

@app.route("/app", methods=["GET"])
def index():
    if not session:
        return render_template("login.html")

    elif session["isAdmin"] == True:
        return render_template("admin.html")

    else:
        return render_template("guest.html")


@app.route("/app/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "" or password == "":
            return render_template("login.html", msg="Enter username and password")
        try:
            values = {}
            values.update(request.form.to_dict(flat=True))
            user = get_user('SELECT * FROM users WHERE username=:username AND password=:password',values, one=True)

            if user:
                if user[2]:
                    session["username"] = user[0]
                    session["isAdmin"] = True
                    session["login"] = True
                    return redirect("/app/admin")
                else:
                    session["username"] = user[0]
                    session["isAdmin"] = False
                    session["login"] = True
                    return redirect("/app/guest")
            else:
                return render_template("login.html", msg="Login Failed..."), 401
        except Exception as e:
            print(e,flush=True)
            abort(500)

@app.route("/app/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "" or password == "":
            return render_template("signup.html", msg="Enter username and password")
        
        values = {'isAdmin': 0}
        values.update(request.form.to_dict(flat=True))
        try:
            insert_user('INSERT INTO users VALUES (:username, :password, :isAdmin)',values)
        except Exception as e:
            print(e,flush=True)
            return render_template("signup.html", msg="Something Error")
        
        return redirect('/app/login')


@app.route("/app/guest", methods=["GET"])
def guest():
    if not session:
        return redirect("/app/login")

    return render_template("guest.html")


@app.route("/app/admin", methods=["GET", "POST"])
def admin():
    if not session:
        return redirect("/app/login")

    if session["isAdmin"] == False:
        return redirect("/app/guest")

    if request.method == "GET":
        return render_template("admin.html")
    else:
        if not request.cookies['X-CURL-TOKEN'] or request.cookies['X-CURL-TOKEN'] != '[**REDACTED**]':
            return render_template('admin.html', msg='Token is not valid')
        scheme = request.form['scheme'].strip()
        host = request.form['host'].strip()
        port = request.form['port'].strip()
        path = request.form['path'].strip()

        if scheme == '' or host == '' or port == '':
            return redirect('/app/admin')
        
        url = build_url(scheme, host, port, path)
        if url:
            for chr in ['@', '{', '}', ',']:
                if chr in url:
                    return render_template('admin.html', msg='Not allowed string or character')
            try:
                response = run(
                    ["curl", f"{url}"], capture_output=True, text=True, timeout=1
                )
                return render_template('admin.html', response=response.stdout)

            except TimeoutExpired:
                return render_template('admin.html', msg='Timeout')
            
        return render_template('admin.html', msg='Did not build the URL')


@app.route('/app/flag', methods=['GET'])
def flag():
    ip = ip_address(request.remote_addr)
    if ip.is_private:
        FLAG = open('./flag.txt','r').read()
        return FLAG
    else:
        return f"Only local access allowed", 403

        


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port='8002')