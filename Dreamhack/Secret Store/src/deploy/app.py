from flask import Flask, request, jsonify, render_template,session,redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "**redacted**"

banlist = [
    '!', '"', '$', '%', '&', '+', '.', ':', '<', '>', '?', '@', '[', '\\', ']',
    '^', '_', '`', '|', '~',
    'alter', 'as', 'benchmark', 'case', 'count', 'create', 'cursor', 'database',
    'declare', 'delay', 'delete', 'describe', 'drop', 'exec', 'extract',
    'fetch','id','if', 'insert', 'lite', 'master', 'pragma', 'set', 'sleep', 'sql',
    'table', 'update', 'wait','grade','name'
]

def get_db_connection():
    conn = sqlite3.connect("fruits.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')

        if username.lower() == "admin":
            username = ""

        username_upper = username.upper()
        
        if username_upper == 'ADMIN':
            session['user'] = username_upper
            return redirect(url_for('search'))
        else:
            return ("<p>Login failed</p>")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route("/search", methods=["GET", "POST"])
def search():
    if 'user' not in session or session['user'] != 'ADMIN':
        return jsonify({"error": "unauthorized"}), 401
    
    if request.method == "GET":
        return render_template("index.html")

    name = request.form.get("name", "")
    lowered = name.lower()
    
    for bad in banlist:
        if bad in lowered:
            name = ""
            break

    query = f"SELECT id, name, grade FROM gyul WHERE name = '{name}'"

    conn = get_db_connection()
    rows = conn.execute(query).fetchall()
    conn.close()

    exists = len(rows) > 0

    return jsonify({
        "exists": exists
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=False)