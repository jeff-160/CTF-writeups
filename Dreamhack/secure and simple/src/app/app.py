from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from pymongo import MongoClient
import os
from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime
from sympy import nextprime
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)

def generate_key(bits):
    p = getPrime(bits//2)
    q = getPrime(bits//2)
    N = p * q
    e = nextprime(1337)
    
    return (N, e)

def encrypt(s):
    ls=bytes_to_long(s)
    if ls >= KEY[0]:
        raise ValueError("Message must be less than N")
    return long_to_bytes(pow(ls, KEY[1], KEY[0]))

FLAG = "WaRP{REDACTED}"
KEY = generate_key(512)

client = MongoClient('mongodb://mongo:27017/')
db = client.myapp
users = db.users

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in first!')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users.find_one({'username': username})
        if user and user['password'] == encrypt(password.encode()).hex():
            session['username'] = username
            flash('Successfully logged in!')
            return redirect(url_for('flag'))
        else:
            flash('Invalid credentials!')
    
    return render_template('login.html')

@app.route('/getkey')
def givekey():
    return render_template('getkey.html', username=session.get('username'), N=KEY[0], e=KEY[1])

@app.route('/flag')
@login_required
def flag():
    return render_template('flag.html', username=session.get('username'), flag=FLAG)

@app.route('/search')
def search():
    q=request.args["q"]
    foundUsers = users.find({'$where':"function(){return this.username.includes('"+q+"')}"})
    return render_template('search.html', users=foundUsers)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out!')
    return redirect(url_for('index'))

time.sleep(10)
client = MongoClient('mongodb://mongo:27017/')
db = client.myapp
users = db.users
pw=b'REDACTED'

users.insert_one({
    'username': 'admin',
    'password': encrypt(pw).hex()
})
users.insert_one({
    'username': 'guest',
    'password': encrypt(long_to_bytes(bytes_to_long(pw)*365 + 1337)).hex()
})

app.run(host='0.0.0.0', port=8000)