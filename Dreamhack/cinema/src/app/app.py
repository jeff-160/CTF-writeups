from flask import Flask, request, render_template, Response
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import datetime
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='visitor_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

with open('flag.txt', 'r') as file:
    FLAG = file.read().strip()

with open('review.txt','r') as f:
    REVIEWS = f.read().strip()

@app.after_request
def set_headers(response):
    csp = (
        "script-src 'self' https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.1.6/purify.min.js; "
        "style-src 'unsafe-inline'; "
        "font-src 'none'; "
        "media-src 'self';"
    )
    response.headers['Content-Security-Policy'] = csp
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Document-Policy'] = 'force-load-at-top'
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/')
def index():
    log_visit()
    return render_template('index.html')

@app.route('/review', methods=["GET"])
def review():
    log_visit()
    text = request.args.get('text', '')
    
    if not isinstance(text, str):
        return 'string... plz', 200

    if len(text) < 20:
        return 'Tooooo short... plz', 200

    if len(text) > 50:
        return 'Tooooo long... plz', 200

    for char in text:
        char_code = ord(char)
        if (char_code < 9 or (char_code > 13 and char_code < 32) or char_code > 127):
            return 'ASCII...plz', 200
    
    if request.remote_addr == '127.0.0.1':
        response_text = f"{text} {FLAG}"
    else:
        response_text = f"{text} {REVIEWS}"

    response = Response(response_text.encode('utf-8'))
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response

@app.route("/report", methods=["GET", "POST"])
def report():
    log_visit()
    if request.method == "POST":
        path = request.form.get("path")
        if not path:
            return render_template("report.html", msg="fail")

        if path.startswith("/"):
            path = path[1:]

        url = f"http://127.0.0.1/{path}"
        if check_url(url):
            return render_template("report.html", msg="success")
        else:
            return render_template("report.html", msg="fail")
    else:
        return render_template("report.html")

def check_url(url):
    try:
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-features=BlockInsecurePrivateNetworkRequests')
        options.add_argument('--incognito')
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(3)
        driver.get(url)
        sleep(1)
        return True
    except Exception as e:
        return False
    finally:
        driver.quit()

def log_visit():
    ip_address = request.remote_addr
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"IP: {ip_address} - Path: {request.path}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)