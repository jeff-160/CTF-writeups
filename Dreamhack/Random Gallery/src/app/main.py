from flask import Flask, request, redirect, session
from config import SECRET_KEY, FLAG, ADMIN_PASSWORD
import os
import random

app = Flask(__name__)
app.secret_key = SECRET_KEY

users = {
    "admin": ADMIN_PASSWORD
}

os.remove("config.py")

@app.route('/')
def index():
    if "username" not in session:
        return redirect('/login')
    return f"<img src='/static/{random.randint(0, 5)}.jpg' />"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
            <form method="post">
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <input type="submit" value="Login">
            </form>
            <a href="/register">Register</a>
        '''
    
    username = request.form.get('username')
    password = request.form.get('password')
    if users.get(username) == password:
        session["username"] = username
        return redirect('/')
    else:
        return "<script>alert('Invalid credentials');history.go(-1);</script>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return '''
            <form method="post">
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <input type="submit" value="Register">
            </form>
        '''
    
    username = request.form.get('username')
    password = request.form.get('password')
    if username in users:
        return "<script>alert('Username already exists');history.go(-1);</script>"
    users[username] = password
    return redirect('/login')
    
@app.route('/flag', methods=['GET'])
def flag():
    if session.get("username") != "admin":
        return redirect('/')
    return FLAG