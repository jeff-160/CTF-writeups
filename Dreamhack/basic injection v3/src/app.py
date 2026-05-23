from flask import Flask, request, jsonify, render_template, render_template_string, session
import sqlite3
import os
import threading
import time
import re
from middleware import check

app = Flask(__name__)
app.secret_key = 'REDACTED'

def clean():
    path = '.env'
    if os.path.exists(path):
            with open(path, 'rb') as f:
                e = f.read()
            a = e.decode('utf-8', errors='ignore')
            b = ''.join(char for char in a if char.isprintable() or char in '\n\r\t')
            c = r'[A-Za-z_][A-Za-z0-9_]*=[^\n]*'
            d = re.findall(c, b)
            with open(path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(d))

def monitor():
    while True:
        clean()
        time.sleep(0.5)

def init():
    conn = sqlite3.connect('main.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')
    c.execute("INSERT INTO users (username, password, email) VALUES ('admin', 'REDACTED', 'admin@byte256.com')")
    c.execute("INSERT INTO users (username, password, email) VALUES ('user', 'asdf', 'user@byte256.com')")
    conn.commit()
    conn.close()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    email = data.get('email', 'asdf@byte256.com')
    
    try:
        conn = sqlite3.connect('main.db')
        c = conn.cursor()
        query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}')"
        c.executescript(query)
        conn.commit()
        conn.close()
        return jsonify({'status': 'oh'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    
    try:
        conn = sqlite3.connect('main.db')
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        c.execute(query)
        user = c.fetchone()
        conn.close()
        
        if user:
            if not check(user[1]):
                return jsonify({'status': 'error', 'message': 'nope! ヾ (✿＞﹏ ⊙〃)ノ'}), 403
            session['username'] = user[1]
            return jsonify({'status': 'oh', 'username': user[1]})
        else:
            return jsonify({'status': 'error'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/memo')
def memo():
    if session.get('username') != 'admin':
        return 'nope! ヾ (✿＞﹏ ⊙〃)ノ', 403
    memo = request.args.get('memo', '')
    
    return render_template_string(f"""
    <h1>Secret memo (,,◕﹃◕,,)♡</h1>

    <form>
        <textarea name="memo" placeholder="당신의 은밀한 메모를 적어보세요..!" style="width:100%;height:150px;">{memo}</textarea><br><br>
        <button type="button" onclick="location.href='/memo?memo=' + encodeURIComponent(document.querySelector('textarea').value)">Save Memo</button>
    </form>
    
    <hr>
    <h2>Memo</h2>
    <div style="background:#f0f0f0;padding:20px;border-left:5px solid #333;">
        {memo}
    </div>
    """)

init()
create = threading.Thread(target=monitor, daemon=True)
create.start()
app.run(debug=False, host='0.0.0.0', port=5000)