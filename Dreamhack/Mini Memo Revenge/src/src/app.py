import os
import unicodedata
from flask import (
        Flask, render_template, render_template_string, request, redirect,
        url_for, session, flash, get_flashed_messages)
from database import init_db, get_user_db_connection, get_memo_db_connection

app = Flask(__name__)
app.secret_key = os.urandom(32)

app.template_context_processors[None].clear()
app.jinja_env.globals.clear()
app.jinja_env.globals.update({
    'get_flashed_messages': get_flashed_messages,
    'url_for': url_for,
    'session': session})

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('memo_list'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if len(username) > 10:
            flash('Username must be 10 characters or less!')
            return render_template('register.html')
        
        if len(password) > 10:
            flash('Password must be 10 characters or less!')
            return render_template('register.html')

        banned = ['admin', 'config', 'system', 'flag']
        if any(word in unicodedata.normalize('NFKC', username + password).lower() for word in banned):
            flash('Username or password cannot contain reserved words!')
            return render_template('register.html')

        conn = get_user_db_connection()
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'user')", (username, password))
            conn.commit()
            flash('Registration successful!')
            return redirect(url_for('login'))
        except Exception:
            flash('Username already exists!')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if len(username) > 10:
            flash('Username must be 10 characters or less!')
            return render_template('login.html')

        conn = get_user_db_connection()
        c = conn.cursor()
        c.execute("SELECT id, username, role FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[2]
            return redirect(url_for('memo_list'))
        else:
            flash('Invalid credentials!')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/memos')
def memo_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_memo_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, content FROM memos WHERE user_id = ?", (session['user_id'],))
    memos = c.fetchall()
    conn.close()

    return render_template('memo_list.html', memos=memos)

@app.route('/memo/new', methods=['GET', 'POST'])
def memo_new():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        template = request.form['template']

        conn = get_memo_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO memos (user_id, title, content, template) VALUES (?, ?, ?, ?)",
                  (session['user_id'], title, content, template))
        conn.commit()
        conn.close()

        return redirect(url_for('memo_list'))

    return render_template('memo_new.html')

@app.route('/memo/<int:memo_id>')
def memo_view(memo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_memo_db_connection()
    c = conn.cursor()
    c.execute("SELECT title, content, template FROM memos WHERE id = ? AND user_id = ?",
              (memo_id, session['user_id']))
    memo = c.fetchone()
    conn.close()

    if not memo:
        return "Memo not found", 404

    title, content, template = memo

    template_path = f"data/templates/{template}"

    if template.startswith("/") or template.startswith("../"):
        template_path = f"data/templates/default"

    template_path = os.path.normpath(template_path)
    if not template_path.startswith("data/"):
        template_path = "data/templates/default"

    try:
        with open(template_path, 'r', encoding='utf-8', errors='ignore') as f:
            template_content = f.read()
    except FileNotFoundError:
        with open("data/templates/default", 'r', encoding='utf-8') as f:
            template_content = f.read()

    rendered_memo = render_template_string(template_content, title=title, content=content)

    return rendered_memo

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('data/templates'):
        os.makedirs('data/templates')

    init_db()
    app.run(host='0.0.0.0', port=5000)
