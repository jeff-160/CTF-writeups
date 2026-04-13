from flask import Flask, request, render_template, redirect, url_for, session, flash
from playwright.sync_api import sync_playwright, Playwright
import time
import os
import threading
from sanitizer import sanitize_input
from functools import wraps

# Single persistent browser instance shared across all requests
_playwright_lock = threading.Lock()
_playwright_instance: Playwright = None
_browser = None

def get_browser():
    global _playwright_instance, _browser
    with _playwright_lock:
        if _browser is None or not _browser.is_connected():
            # Browser reconnected — invalidate cached session too
            _invalidate_storage_state()
            _playwright_instance = sync_playwright().start()
            _browser = _playwright_instance.chromium.launch(
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-extensions",
                ],
                headless=True,
            )
    return _browser

# Pre-authenticated admin session state — created once, stamped into every new context
_storage_state_lock = threading.Lock()
_admin_storage_state = None

def _invalidate_storage_state():
    global _admin_storage_state
    _admin_storage_state = None

def get_admin_storage_state():
    """Login as admin once, cache the cookie state. Each context gets its own isolated copy."""
    global _admin_storage_state
    if _admin_storage_state is not None:
        return _admin_storage_state
    with _storage_state_lock:
        if _admin_storage_state is not None:  # double-checked locking
            return _admin_storage_state
        browser = get_browser()
        ctx = browser.new_context()
        page = ctx.new_page()
        page.goto("http://127.0.0.1:3000/login")
        page.fill('[name=username]', 'admin')
        page.fill('[name=password]', ADMIN_PASS)
        page.click('button[type=submit], input[type=submit]')
        page.wait_for_url('**/**', timeout=5000)
        _admin_storage_state = ctx.storage_state()  # snapshot: {cookies: [...], origins: [...]}
        ctx.close()
        print("[bot] Admin session pre-authenticated and cached")
    return _admin_storage_state


FLAG = os.environ.get('FLAG') or open('flag.txt').read().strip() if os.path.exists('flag.txt') else 'flag{test_flag}'

app = Flask(__name__)
app.secret_key = os.urandom(32).hex()

users = {}

ADMIN_PASS = os.urandom(32).hex()

SECRET = os.urandom(32).hex()

banlist = [
    "`", "\"", "'", ";", "@", "!", "%", "(", ")", "!", "\\x", "alert", "fetch", "replace",
    "javascript", "location", "href", "window", "innerHTML", "src", "document", "cookie",
    "function", "constructor", "atob", "decodeURI", "decodeURIComponent", "escape", "unescape",
    "setTimeout", "xhr", "XMLHttpRequest", "origin", "this", "self", "proto", "prototype"
]

if "admin" not in users:
    users["admin"] = {"password": ADMIN_PASS}

def is_logged_in():
    return "username" in session

def current_user():
    return session.get("username")
    
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

def _visit_url(url):
    """Actual browser work — called only from a bot worker thread."""
    storage = get_admin_storage_state()
    browser = get_browser()
    context = browser.new_context(storage_state=storage)
    page = context.new_page()
    page.set_default_timeout(5000)
    page.goto(url)
    page.wait_for_timeout(1000)
    context.close()
    return True

def read_url(url):
    """Directly visit URL."""
    try:
        return _visit_url(url)
    except Exception:
        import traceback
        print('[read_url ERROR]', traceback.format_exc())
        return False


@app.route('/')
def home():
    return render_template('home.html', logged_in=is_logged_in(), user=current_user())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '') 
        confirm = request.form.get('confirm', '') 

        if not username or not password:
            return render_template('register.html', message={'type': 'error', 'text': 'Username and password are required.'})

        if password != confirm:
            return render_template('register.html', message={'type': 'error', 'text': 'Passwords do not match.'})

        if username in users:
            return render_template('register.html', message={'type': 'error', 'text': 'Username already exists.'})

        users[username] = {"password": password}
        return render_template('login.html', message={'type': 'success', 'text': 'Registration successful. Please log in.'})

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '') 

        if username not in users:
            return render_template('login.html', message={'type': 'error', 'text': 'Invalid username or password.'})

        if not (users[username]["password"] == password):
            return render_template('login.html', message={'type': 'error', 'text': 'Invalid username or password.'})

        session['username'] = username
        return render_template('home.html', logged_in=is_logged_in(), user=current_user(), message={'type': 'success', 'text': f'Welcome, {username}!'} )

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('home.html', logged_in=is_logged_in(), user=current_user(), message={'type': 'info', 'text': 'Logged out.'})


@app.route('/test', methods=['GET'])
@login_required
def test():
    payload = request.args.get('payload')

    if payload is None:
        return render_template('test.html', result=None, error=None, payload=None)

    for banned in banlist:
        if banned in payload:
            print(f"Banned term detected: {banned}")
            return render_template('test.html', result=None, error=f"Banned term detected: {banned}", payload=payload)

    cleaned = sanitize_input(payload)
    return render_template('test.html', result=cleaned, error=None, payload=payload)

@app.route('/report')
@login_required
def report():
    payload = request.args.get('payload')
    if payload is None:
        return render_template('report.html', message=None, payload=None)

    url = f'http://127.0.0.1:3000/test?payload={payload}'
    result = read_url(url)
    message = "Success" if result else "Fail"
    return render_template('report.html', message=message, payload=payload)

@app.route('/flag')
@login_required
def flag():
    ip = request.remote_addr
    is_localhost = ip == '127.0.0.1'
    username = current_user()

    if is_localhost and username == 'admin':
        return render_template('flag.html', flag=FLAG, username=username)

    return render_template('flag.html', flag=None, username=username)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
