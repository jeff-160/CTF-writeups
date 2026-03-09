from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from os import urandom
from urllib.parse import quote
from filter import xss_filter_keyword, xss_filter_tag

app = Flask(__name__)
app.secret_key = urandom(32)

try:
    FLAG = open('./flag.txt','r').read()
except:
    FLAG = 'DH{fake_flag}'

@app.route('/xss', methods=["GET"])
def xss():
    content = request.args.get('content')
    clean = xss_filter_keyword(xss_filter_tag(content))
    return jsonify({"content": clean})

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

    

def access_page(content, cookie={"name": "name", "value": "value"}):
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
        driver.get(f"http://127.0.0.1:8000/")
        driver.add_cookie(cookie)
        driver.get(f"http://127.0.0.1:8000/?content={quote(content)}")
        sleep(1)
    except Exception as e:
        print(e, flush=True)
        driver.quit()
        return False
    driver.quit()
    return True



@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        param = request.form.get("content")
        if not param:
            return render_template("report.html", msg="fail")
        else:
            if access_page(param, cookie={"name": "flag", "value": FLAG}):
                return render_template("report.html", msg="Success")
            else:
                return render_template("report.html", msg="fail")
    else:
        return render_template("report.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)