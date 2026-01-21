from flask import *
import jwt
import re
import string
import random
from datetime import datetime, timedelta
import subprocess
import os

request_count = 0
timeout_until = None
app = Flask(__name__)

RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_TIMEOUT = timedelta(minutes=5)

JWTKey = ''.join(random.choices(string.ascii_letters, k=50))
app.config['JWTKey'] = JWTKey

users = [
    {"id": "admin", "pw": "{{REDACTED}}"},
    {"id": "guest", "pw": "guest"},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if request.cookies.get('auth'):
            return render_template_string('<script>alert("You are already logged in.");history.back()</script>')
        return render_template('login.html')
    elif request.method == 'POST':
        form_id = request.form['id']
        form_pw = request.form['pw']
        print(form_id, form_pw)
        if len(form_id) > 10:
            return "Too Long"
        elif len(form_id) < 3:
            return "Too Short"
        elif not re.search(r"^[A-Za-z{}]*$", form_id):
            return "Blacklist Word"

        user = next((user for user in users if user['id'] == form_id), None)
        if user and user['pw'] == form_pw:
            payload = {
                'id': form_id,
                'isAdmin': (form_id == 'admin'),
            }
            encode_jwt = jwt.encode(payload, JWTKey, algorithm='HS256')
            resp = make_response(render_template_string('Login Success!'))
            resp.set_cookie('auth', encode_jwt)
            return resp
        else:
            return render_template_string('{form_id} is not registered, or the password is incorrect.'.format(form_id=form_id))
        
@app.route('/logout')
def logout():
    resp = make_response(render_template_string('<script>alert("Bye.");history.back()</script>'))
    resp.set_cookie('auth', '', expires=0)
    return resp
        
@app.route('/dashboard', methods=['GET', 'POST'])
def admin():
    if request.cookies.get('auth'):
        try:
            decode_jwt = jwt.decode(request.cookies.get('auth'), JWTKey, algorithms=['HS256'])
            if decode_jwt['id'] == 'admin' and decode_jwt['isAdmin'] == True:
                return render_template('admin.html')
            else:
                return render_template_string('You are not admin.')
        except:
            return send_file("./cat/fail.jpg", mimetype='image/jpg') # BAD JWT
    else:
        return render_template_string('<script>alert("You are not logged in.");history.back()</script>')

@app.route('/api/metar')
def metar():
    global request_count
    global timeout_until
    current_time = datetime.now()
    if timeout_until and current_time < timeout_until:
        remaining_time = timeout_until - current_time
        return "Timeout! {}".format(remaining_time), 429
    if request.cookies.get('auth'):
        try:
            decode_jwt = jwt.decode(request.cookies.get('auth'), JWTKey, algorithms=['HS256'])
            if decode_jwt['id'] == 'admin' and decode_jwt['isAdmin'] == True:
                request_count += 1
                if request_count >= RATE_LIMIT_REQUESTS:
                    timeout_until = current_time + RATE_LIMIT_TIMEOUT
                    request_count = 0 
                airport = request.args.get('airport')
                result = subprocess.run(['curl', airport], shell = False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)                    
                return result.stdout
            else:
                return render_template_string('You are not admin.')
        except Exception as e:
            print(e)
            return send_file("./cat/fail.jpg", mimetype='image/jpg') # BAD JWT
    else:
        return render_template_string('<script>alert("You are not logged in.");history.back()</script>')
    
app.run(host='0.0.0.0', port=13000, threaded=False)