import os
import pickle
from flask import session,Flask, request, render_template, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import uuid
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB limit
app.secret_key = os.urandom(24)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# This is a placeholder for a class that might be used.
# The vulnerability remains the direct unpickling of the file.
class ArtPiece:
    def __init__(self, title, content, image_filename=None):
        self.title = title
        self.content = content
        self.image_filename = image_filename

    def __repr__(self):
        return f"ArtPiece(title='{self.title}', image='{self.image_filename}')"

@app.before_request
def before_request():
    if session.get('uuid') is None:
        session['uuid'] = str(uuid.uuid4())

@app.route('/')
def index():
    uploaded_files = []
    uploads_dir = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    if os.path.exists(uploads_dir):
        for filename in os.listdir(uploads_dir):
            if not filename.startswith(session['uuid']):
                continue
            filepath = os.path.join(uploads_dir, filename)
            if os.path.isfile(filepath) and not filename.startswith('.'):
                uploaded_files.append(filename)
    return render_template('index.html', files=uploaded_files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        flash('No file part in request.')
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        flash('No file selected.')
        return redirect(request.url)

    if file:
        filename = secure_filename(session['uuid'] + '_' + file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        flash(f"Art piece '{filename}' submitted successfully! Visit /view/{filename} to process it for the gallery.")
    return redirect(url_for('index'))

@app.route('/view/<filename>')
def view_file(filename):
    if not filename.startswith(session['uuid'] + '_'):
        flash('Unauthorized access to this art piece.')
        return redirect(url_for('index'))
    safe_filename = secure_filename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
    if not os.path.exists(filepath):
        flash('Art piece not found.')
        return redirect(url_for('index'))
    try:
        with open(filepath, 'rb') as f:
            pickled_data = f.read()
        deserialized_object = pickle.loads(pickled_data)
        return f"<h3>Art piece '{safe_filename}' has been processed for display!</h3><p>Object representation: {deserialized_object}</p>"
    except pickle.UnpicklingError as e:
        return f"<h3>Error processing '{safe_filename}':</h3><p>This does not appear to be a valid art format. ({e})</p>"
    except Exception as e:
        return f"<h3>An unexpected error occurred while processing '{safe_filename}':</h3><p>Error details: {e}</p>"

@app.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)