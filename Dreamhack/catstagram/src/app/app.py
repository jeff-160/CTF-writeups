from flask import *
from functools import wraps
import secrets
import os
from db import *

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(20)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
init_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('register'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        username = session['user']
        user_role = get_user_role(username)
        if user_role != 'admin':
            flash('Access denied. Administrator privileges required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not isinstance(username, str) or not isinstance(password, str):
            flash('Invalid input format. Please try again.', 'error')
            return render_template('register.html')
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('register.html')
        if len(username) < 3 or len(password) < 3:
            flash('Username and password must be at least 3 characters long.', 'error')
            return render_template('register.html')
        if not is_user_exists(username):
            add_user(username, password)
            session['user'] = username
            flash('Registration successful! Welcome to Catstagram!', 'success')
            return redirect(url_for('dashboard'))
        flash('Username already exists. Please choose a different username.', 'error')
        return render_template('register.html')
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not isinstance(username, str) or not isinstance(password, str):
            flash('Invalid input format. Please try again.', 'error')
            return render_template('login.html')
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('login.html')
        if authenticate_user(username, password):
            session['user'] = username
            flash('Login successful! Welcome back!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password. Please try again.', 'error')
        return render_template('login.html')
    return render_template('login.html')

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        action = request.args.get('action')
        if action == 'like':
            cat_id = request.form['cat_id']
            new_like_count = like_cat(cat_id)
            return jsonify({'status': 'success', 'new_like_count': new_like_count, 'cat_id': cat_id})
        elif action == 'upload':
            file = request.files['cat_image']
            if file and file.filename:
                filename = file.filename.lower()
                prohibited_extensions = ['.html', '.py', '.js', '.css', '.json', '.sh', '.sql', '.xml', '.txt']
                if any(filename.endswith(ext) for ext in prohibited_extensions):
                    flash('Invalid file type. Please upload only image files (jpg, png, gif, etc.).', 'error')
                    return redirect(url_for('dashboard'))
                original_filename = file.filename
                file_extension = os.path.splitext(original_filename)[1].lower()
                file_basename = os.path.splitext(original_filename)[0]
                counter = 0
                final_filename = original_filename
                while is_filename_exists(final_filename):
                    counter += 1
                    final_filename = f"{file_basename}-{counter}{file_extension}"
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], final_filename))
                cat_name = request.form.get('cat_name', 'Cute Cat')
                description = request.form.get('description', 'A wonderful cat moment!')
                owner = session.get('user', 'Anonymous')
                try:
                    add_cat_post(cat_name, owner, description, final_filename)
                    flash('Your cat photo has been shared successfully!', 'success')
                except Exception:
                    flash("Can't add post. Please try again.", 'error')
                return redirect(url_for('dashboard'))
            flash('Please select a file to upload.', 'error')
            return redirect(url_for('dashboard'))
        return "No action given"
    cats = get_cats()
    return render_template("dashboard.html", cats=cats)

@app.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin():
    if request.method == 'POST':
        filename = request.form.get('filename', 'cats.json')
    else:
        filename = 'cats.json'
    cats = get_cats()
    try:
        with open(filename, 'r') as file:
            file_content = file.read()
        return render_template('admin.html', filename=filename, file_content=file_content, user=session.get('user'), cats=cats)
    except FileNotFoundError:
        flash(f'File "{filename}" not found.', 'error')
        return render_template('admin.html', filename=filename, file_content='File not found', user=session.get('user'), cats=cats)
    except Exception as e:
        flash(f'Error reading file: {str(e)}', 'error')
        return render_template('admin.html', filename=filename, file_content=f'Error: {str(e)}', user=session.get('user'), cats=cats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)