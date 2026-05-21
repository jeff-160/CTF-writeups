from flask import Flask, request, render_template
import os
import bleach
import requests

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

DANGER_FILENAMES = ['templates', 'flag']


def check_danger_filename(content):
    for forbidden in DANGER_FILENAMES:
        if forbidden in content:
            return True
    return False


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file provided!", 400

    file = request.files['file']

    if file.filename == '':
        return "No file selected!", 400
	
    if file:
        filepath = file.filename
        filepaths = os.path.abspath(os.path.join(UPLOAD_FOLDER, filepath))
        if ".." in filepaths:
            return "Malicious activity detected.", 401
        
        if check_danger_filename(filepaths):
            return "Malicious activity detected.", 400

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        data = file.read()
        with open(filepaths, 'wb') as f:
            f.write(data)
        return f'<script>alert("File uploaded successfully: {filepath}");location.href="/load-file";</script>'

    return "Invalid file type!", 400

@app.route('/load-file', methods=['GET'])
def load_file_view():
    filepath = request.args.get('filename', '')
    if not filepath:
        return render_template('load_file.html')
    filepaths = os.path.abspath(os.path.join(UPLOAD_FOLDER, filepath))
    print(filepaths, flush=True)

    if ".." in filepath:
        return "Malicious activity detected.", 401

    if not os.path.exists(filepaths):
        return "File does not exist!", 404
    
    if check_danger_filename(filepaths):
        return "Malicious activity detected.", 400

    with open(filepaths, 'r') as file:
        file_content = file.read()
    sanitized_content = bleach.clean(file_content)

    return f"File content:\n{sanitized_content}"


@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        file = request.form['filename']
        response = requests.post("http://bot:9999/report", data={'filename': file})
        return render_template('report.html', message=response.text)
    else:
        return render_template('report.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)