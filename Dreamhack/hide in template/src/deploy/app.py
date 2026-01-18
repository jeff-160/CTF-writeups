import os
from flask import Flask, request, session, render_template, redirect, abort, url_for

from utils import auth, access, validate, set
from theme import Theme
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_is_secret')
app.debug = False

try:
    flag = open('/fakeflag').read()
except:
    flag = 'DH{' + 'fake'*16 +'}'
    
CSS_KEYS = ['color', 'background-color']

# I'm too lazy to use DBMS...
users = {
    'admin': {
        'pw': auth.hash(os.urandom(32).hex()),
        'theme': Theme({'color': 'black', 'background-color': 'black'}), # hide in black...
        'idx': 0,
    },
    'guest': {
        'pw': auth.hash('guest'),
        'theme': Theme({}),
        'idx': 1,
    }
}

for k, v in users.items():
    Theme.add(k, v['theme'])

@app.before_request
def before():
    if session.get('logined', None) is None:
        session['logined'] = False

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', False)
        password = request.form.get('password', False)

        if not (validate(username, min_max=(8, 256)) and validate(password, min_max=(8, 256))):
            return abort(400)
        
        # duplicate users
        if username in users:
            return redirect(url_for('signup'))
        
        theme = Theme({})
        Theme.add(username, theme)
        users[username] = {
            'pw': auth.hash(password),
            'idx': len(users) + 1,
            'theme': theme
        }
        
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session['logined']:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', False)
        password = request.form.get('password', False)

        if not (validate(username, min_max=False) and validate(password, min_max=False)):
            return abort(400)
        
        if username not in users:
            return redirect(url_for('login'))
        
        user = users[username]
        if auth.verify(password, user.get('pw', False)):
            session['idx'] = user.get('idx')
            session['logined'] = True
            session['username'] = username
            
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()

    return redirect(url_for('index'))

@app.route('/theme/edit', methods=['GET', 'POST'])
@access.login_required
def theme_edit():
    if request.method == 'POST':
        key = request.form.get('key', '')
        value = request.form.get('value', '')

        if not (validate(key) and validate(key)):
            abort(400)

        if key not in CSS_KEYS:
            return abort(400)

        username = session.get('username')
        user = users.get(username)

        set(Theme, f'customs.{username}.style.{key}', value)
        
        user['theme'] = Theme.get(username)

        return redirect(url_for('profile'))
    
    return render_template('theme_edit.html')

@app.route('/profile', methods=['GET'])
@access.login_required
def profile():
    theme = Theme.get(session['username']).style
    return render_template('profile.html', theme=theme)

@app.route('/admin', methods=['GET'])
@access.admin_only
def admin():
    return render_template('flag.html', flag=flag)

if __name__ == "__main__":
    app.run("0.0.0.0", port=80)
