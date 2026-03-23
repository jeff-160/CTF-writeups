from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response, jsonify
import os
import subprocess
import uuid
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'),  static_folder='/srv/http/static')

UPLOAD_FOLDER = '/srv/http/uploads'
FRAMES_BASE = '/srv/http/static/frames'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FRAMES_BASE, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'success': False, 'error': 'File too large. Maximum size is 16MB.'}), 413

def get_user_id():
    user_id = request.cookies.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
    return user_id

def extract_frames(input_path, output_dir, gif_name):
    os.makedirs(output_dir, exist_ok=True)
    
    width = 120
    
    cmd = [
        'ffmpeg', '-i', input_path,
        '-vf', f'fps=10,scale={width}:-1:flags=lanczos,palettegen',
        '-y', f'{output_dir}/palette.png'
    ]
    subprocess.run(cmd, capture_output=True)
    
    cmd = [
        'ffmpeg', '-i', input_path,
        '-i', f'{output_dir}/palette.png',
        '-lavfi', f'fps=10,scale={width}:-1:flags=lanczos[x];[x][1:v]paletteuse',
        '-y', f'{output_dir}/output.gif'
    ]
    subprocess.run(cmd, capture_output=True)
    
    frame_count = 0
    cmd = [
        'ffmpeg', '-i', f'{output_dir}/output.gif',
        f'{output_dir}/frame_%04d.png'
    ]
    subprocess.run(cmd, capture_output=True)
    
    for f in os.listdir(output_dir):
        if f.startswith('frame_') and f.endswith('.png'):
            frame_count += 1
    
    return frame_count

@app.route('/')
def index():
    user_id = get_user_id()
    
    view_gif = request.args.get('view')
    view_user_id = request.args.get('view_user_id', user_id)
    view_frames = []
    
    if view_gif:
        view_frames_dir = os.path.join(FRAMES_BASE, view_user_id, view_gif)
        if os.path.exists(view_frames_dir):
            view_frames = sorted([f for f in os.listdir(view_frames_dir) if f.startswith('frame_') and f.endswith('.png')])
    
    default_frames_dir = os.path.join(FRAMES_BASE, 'shared', 'bad-apple')
    default_frames = []
    if os.path.exists(default_frames_dir):
        default_frames = sorted([f for f in os.listdir(default_frames_dir) if f.startswith('frame_') and f.endswith('.png')])
    
    user_frames_dir = os.path.join(FRAMES_BASE, user_id)
    gifs = []
    if os.path.exists(user_frames_dir):
        for gif_name in os.listdir(user_frames_dir):
            gif_path = os.path.join(user_frames_dir, gif_name)
            if os.path.isdir(gif_path):
                frames = [f for f in os.listdir(gif_path) if f.startswith('frame_') and f.endswith('.png')]
                gifs.append({'name': gif_name, 'frame_count': len(frames)})
    
    response = make_response(render_template('index.html', 
        user_id=user_id, 
        default_gif='bad-apple',
        default_frames=default_frames,
        gifs=gifs,
        view_gif=view_gif,
        view_user_id=view_user_id,
        view_frames=view_frames))
    response.set_cookie('user_id', user_id)
    return response

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        user_id = request.cookies.get('user_id')
        if not user_id:
            user_id = str(uuid.uuid4())
        
        user_dir = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
        os.makedirs(user_dir, exist_ok=True)
        
        filepath = os.path.join(user_dir, filename)
        file.save(filepath)
        
        safe_name = os.path.splitext(os.path.basename(filename))[0]
        output_dir = os.path.join(FRAMES_BASE, user_id, safe_name)
        
        if os.path.exists(output_dir) and os.listdir(output_dir):
            return jsonify({'success': False, 'error': 'GIF with this name already exists'}), 400
        
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            extract_frames(filepath, output_dir, safe_name)
            response = make_response(jsonify({'success': True, 'user_id': user_id, 'gif_name': safe_name}))
            response.set_cookie('user_id', user_id)
            return response
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/convert')
def convert():
    user_id = request.args.get('user_id', 'anonymous')
    filename = request.args.get('filename', '')

    input_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(user_id), filename)
    if not os.path.exists(input_path):
        return "File not found", 404

    safe_name = os.path.splitext(os.path.basename(filename))[0]
    output_dir = os.path.join(FRAMES_BASE, user_id, safe_name)
    os.makedirs(output_dir, exist_ok=True)

    try:
        frame_count = extract_frames(input_path, output_dir, safe_name)
        return redirect(url_for('index', view=safe_name, user_id=user_id))
    except Exception as e:
        return f"Error processing file: {str(e)}", 500

@app.route('/get_frames')
def get_frames():
    user_id = request.args.get('user_id', 'anonymous')
    gif_name = request.args.get('gif_name', '')
    
    frames_dir = os.path.join(FRAMES_BASE, user_id, gif_name)
    
    if not os.path.exists(frames_dir):
        return jsonify({'error': 'GIF not found'}), 404
    
    frames = sorted([f for f in os.listdir(frames_dir) if f.startswith('frame_') and f.endswith('.png')])
    
    return jsonify(frames)

application = app
