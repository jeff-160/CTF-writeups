from flask import Flask, request
import os
import subprocess

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/", methods=["GET"])
def index():
    cmd = ['python3'] + list(request.args.keys())
    cmd[1] += '.py'
    
    filter_codes = ['`', '$', '<', '>', '|', '&', '{', '}', '=', '*', '?', '!', ';', '"', "'", ',', '\n', '[', ']', '(', ')', '%', '+', 'http', 'flag']
    for filter_code in filter_codes:
        for arg in cmd:
            if filter_code in arg.lower():
                return 'No hack _(:3)J'
    
    if os.path.exists(cmd[1]) == False:
        return 'No such file _(:3)J'
    
    response = subprocess.run(
        cmd, capture_output=True, text=True
    )
    return response.stdout

app.run(host="0.0.0.0", port=9000)
