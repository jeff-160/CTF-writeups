from flask import Flask, request, session, redirect, url_for, render_template
import re
import hashlib
import os
from db import query

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            if not re.match(r"^[a-zA-Z0-9\\ \\-]+$", username):
                raise Exception("Invalid username or password")

            if not re.match(r"^[a-zA-Z0-9\\ \\-]+$", password):
                raise Exception("Invalid username or password")

            result = query(f"SELECT username FROM users WHERE username = '{username}' AND password = '{password}'")
            if len(result) == 0:
                raise Exception("Invalid username or password")
            session['username'] = result[0]['username']
            return redirect(url_for('index'))
        except Exception as e:
            return render_template('login.html', error=str(e))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            if not re.match(r"^[a-zA-Z0-9\\ \\-]+$", username):
                raise Exception("Invalid username or password")

            if not re.match(r"^[a-zA-Z0-9\\ \\-]+$", password):
                raise Exception("Invalid username or password")

            query(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
            return redirect(url_for('login'))
        except Exception as e:
            return render_template('register.html', error=str(e))

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/flag', methods=['GET'])
def flag():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    if session['username'] != 'admin':
        return redirect(url_for('index'))
    
    return os.getenv('FAKE_FLAG')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)