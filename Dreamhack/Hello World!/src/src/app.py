from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    try:
        result = subprocess.run(
            args=["python3", "./hello.py"], capture_output=True, text=True
        )
        return result.stdout
    
    except:
        return "error!"
    
@app.route("/write", methods=["GET"])
def write():
    data = request.args.get('data')
    file = request.args.get('file')

    if os.path.exists(file):
        return "bad"
        
    with open(file, 'w') as f:
        f.write(data)
    
    return "good!"
    
    
app.run(host="0.0.0.0", port=8000)