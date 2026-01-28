#!/usr/bin/python3
from flask import Flask
import hashlib

app = Flask(__name__)


@app.route('/')
def index():
    return "ADMIN PAGE!"

@app.route('/keygen/<path:string>')
def keygen(string):
    n = len(string)-1
    a = hashlib.md5(string.encode('utf-8'))
    return str(hex(int(int(a.hexdigest(),16)/n)))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8000)
