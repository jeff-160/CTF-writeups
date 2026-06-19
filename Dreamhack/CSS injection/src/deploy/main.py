#!/usr/bin/python3
import hashlib, os, binascii, random, string
from flask import Flask, request, render_template, redirect, url_for, session, g, flash
from functools import wraps
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from promise import Promise
from time import sleep

app = Flask(__name__)
app.secret_key = os.urandom(32)

DATABASE = os.environ.get("DATABASE", "database.db")

try:
    FLAG = open("./flag.txt", "r").read().strip()
except:
    FLAG = "[**FLAG**]"

ADMIN_USERNAME = "administrator"
ADMIN_PASSWORD = binascii.hexlify(os.urandom(32))


def execute(query, data=()):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(query, data)
    con.commit()
    data = cur.fetchall()
    con.close()
    return data


def token_generate():
    while True:
        token = "".join(random.choice(string.ascii_lowercase) for _ in range(8))
        token_exists = execute(
            "SELECT * FROM users WHERE token = :token;", {"token": token}
        )
        if not token_exists:
            return token


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if session and session["uid"]:
            return view(**kwargs)
        flash("login first !")
        return redirect(url_for("login"))

    return wrapped_view


def apikey_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        apikey = request.headers.get("API-KEY", None)
        token = execute("SELECT * FROM users WHERE token = :token;", {"token": apikey})
        if token:
            request.uid = token[0][0]
            return view(**kwargs)
        return {"code": 401, "message": "Access Denined !"}

    return wrapped_view


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.context_processor
def background_color():
    color = request.args.get("color", "white")
    return dict(color=color)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user = execute(
            "SELECT * FROM users WHERE username = :username and password = :password;",
            {
                "username": username,
                "password": hashlib.sha256(password.encode()).hexdigest(),
            },
        )

        if user:
            session["uid"] = user[0][0]
            session["username"] = user[0][1]
            return redirect(url_for("index"))

        flash("Wrong username or password !")
        return redirect(url_for("login"))


@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Logout !")
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        user = execute(
            "SELECT * FROM users WHERE username = :username;", {"username": username}
        )
        if user:
            flash("Username already exists !")
            return redirect(url_for("register"))

        token = token_generate()
        sql = "INSERT INTO users(username, password, token) VALUES (:username, :password, :token);"
        execute(
            sql,
            {
                "username": username,
                "password": hashlib.sha256(password.encode()).hexdigest(),
                "token": token,
            },
        )
        flash("Register Success.")
        return redirect(url_for("login"))


@app.route("/mypage")
@login_required
def mypage():
    user = execute("SELECT * FROM users WHERE uid = :uid;", {"uid": session["uid"]})
    return render_template("mypage.html", user=user[0])


@app.route("/memo", methods=["GET", "POST"])
@login_required
def memopage():
    if request.method == "GET":
        memos = execute("SELECT * FROM memo WHERE uid = :uid;", {"uid": session["uid"]})
        return render_template("memo.html", memos=memos)
    else:
        memo = request.form.get("memo")
        sql = "INSERT INTO memo(uid, text) VALUES(:uid, :text);"
        execute(sql, {"uid": session["uid"], "text": memo})
    return redirect(url_for("memopage"))


# report
@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        path = request.form.get("path")
        if not path:
            flash("fail.")
            return redirect(url_for("report"))

        if path and path[0] == "/":
            path = path[1:]

        url = f"http://127.0.0.1:8000/{path}"
        if check_url(url):
            flash("success.")
        else:
            flash("fail.")
        return redirect(url_for("report"))

    elif request.method == "GET":
        return render_template("report.html")


def check_url(url):
    try:
        service = Service(executable_path="/chromedriver-linux64/chromedriver")
        options = webdriver.ChromeOptions()
        for _ in [
            "headless",
            "window-size=1920x1080",
            "disable-gpu",
            "no-sandbox",
            "disable-dev-shm-usage",
        ]:
            options.add_argument(_)
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(3)
        driver.set_page_load_timeout(3)

        driver_promise = Promise(driver.get("http://127.0.0.1:8000/login"))
        driver_promise.then(
            driver.find_element(By.NAME, "username").send_keys(str(ADMIN_USERNAME))
        )
        driver_promise.then(
            driver.find_element(By.NAME, "password").send_keys(ADMIN_PASSWORD.decode())
        )
        driver_promise = Promise(driver.find_element(By.ID, "submit").click())
        sleep(0.1)
        driver_promise.then(driver.get(url))

    except Exception as e:
        driver.quit()
        return False
    finally:
        driver.quit()
    return True


# API
@app.route("/api/me")
@apikey_required
def APIme():
    user = execute("SELECT * FROM users WHERE uid = :uid;", {"uid": request.uid})
    if user:
        return {"code": 200, "uid": user[0][0], "username": user[0][1]}
    return {"code": 500, "message": "Error !"}


@app.route("/api/memo")
@apikey_required
def APImemo():
    memos = execute("SELECT * FROM memo WHERE uid = :uid;", {"uid": request.uid})
    if memos:
        memo = []
        for tmp in memos:
            memo.append({"idx": tmp[0], "memo": tmp[2]})
        return {"code": 200, "memo": memo}

    return {"code": 500, "message": "Error !"}


# For Challenge
def init():
    execute("DROP TABLE IF EXISTS users;")
    execute(
        """
        CREATE TABLE users (
            uid INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            token TEXT NOT NULL UNIQUE
        );
    """
    )

    execute("DROP TABLE IF EXISTS memo;")
    execute(
        """
        CREATE TABLE memo (
            idx INTEGER PRIMARY KEY,
            uid INTEGER NOT NULL,
            text TEXT NOT NULL
        );
    """
    )

    # Add admin
    execute(
        "INSERT INTO users (username, password, token)"
        "VALUES (:username, :password, :token);",
        {
            "username": ADMIN_USERNAME,
            "password": hashlib.sha256(ADMIN_PASSWORD).hexdigest(),
            "token": token_generate(),
        },
    )

    adminUid = execute(
        "SELECT * FROM users WHERE username = :username;", {"username": ADMIN_USERNAME}
    )

    # Add FLAG
    execute(
        "INSERT INTO memo (uid, text)" "VALUES (:uid, :text);",
        {"uid": adminUid[0][0], "text": "FLAG is " + FLAG},
    )


with app.app_context():
    init()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
