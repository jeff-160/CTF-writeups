from flask import Flask, request, render_template, session, redirect, abort
from query import get_user_by_id, add_user, get_user_by_id_and_pw, get_bread_by_name
from bs4 import BeautifulSoup
from os import urandom
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from promise import Promise
from time import sleep

app = Flask(__name__)
app.secret_key = urandom(32)


def check_possibility_xss(memo_text):
    soup = BeautifulSoup(memo_text, "html.parser")
    return bool([tag.name for tag in soup.find_all()])


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/", methods=["GET"])
def index():
    if not session:
        return redirect("/login")
    else:
        return render_template("bread.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

    if username == "" or password == "":
        return render_template("login.html", msg="Enter the username and password")

    try:
        user = get_user_by_id_and_pw(username, password)
        print(user, flush=True)

        if user:
            if user[1] == "admin":
                session["username"] = user[1]
                session["isAdmin"] = True
                return redirect("/bread")
            else:
                session["username"] = user[1]
                session["isAdmin"] = False
                return redirect("/bread")
        else:
            return render_template("login.html", msg="Login Failed..."), 401

    except Exception as e:
        abort(500)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "" or password == "":
            return render_template("signup.html", msg="Enter the username and password")

        try:
            user = get_user_by_id(username)
            if user == None:
                add_user(username, password)
                return redirect("/login")

            elif username == user[0]:
                return render_template("signup.html", msg="Duplicated username"), 403

        except Exception as e:
            print(e, flush=True)
            abort(500)


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("isAdmin", None)
    return redirect("/")


@app.route("/memo")
def memo():
    text = request.args.get("memo", "")
    if check_possibility_xss(text):
        return render_template(
            "memo.html", memo="[REDACTED] - A text with potential for XSS"
        )
    else:
        return render_template("memo.html", memo=text)


@app.route("/bread", methods=["GET"])
def bread():
    if not session:
        return redirect("/login")

    if request.remote_addr != "127.0.0.1":
        return render_template("403.html"), 403

    if request.method == "GET":
        bread_name = request.args.get("bread_name")

        if bread_name == None:
            return render_template("bread.html")

        bread = get_bread_by_name(bread_name)
        print(bread, flush=True)

        if bread == None:
            abort(404)

        if bread[0] and session["isAdmin"]:
            ## It's still under development, so I need to set it up temporarily.
            abort(404)
        else:
            return render_template("bread.html")

    else:
        abort(500)


@app.route("/report", methods=["GET", "POST"])
def report():
    if not session:
        return redirect("/login")

    if request.method == "POST":
        text = request.form.get("memo")
        if not text:
            return render_template("report.html", msg="fail")

        url = f"http://127.0.0.1:8000/memo?memo={text}"

        if check_url(url):
            return render_template("report.html", msg="success")
        else:
            return render_template("report.html", msg="fail")

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
        driver_promise.then(driver.find_element(By.NAME, "username").send_keys("admin"))
        driver_promise.then(
            driver.find_element(By.NAME, "password").send_keys(
                "[**REDACTED**]"
            )
        )
        driver_promise.then(driver.find_element(By.ID, "submit").click())
        driver_promise.then(driver.get(url))
        driver_promise.then(sleep(1))

    except Exception as e:
        driver.quit()
        return False
    finally:
        driver.quit()
    return True


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
