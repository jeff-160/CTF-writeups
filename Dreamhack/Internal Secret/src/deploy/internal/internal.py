from flask import Flask, request, jsonify
import os

app = Flask(__name__)
INTERNAL_IP = "127.0.0.1"

@app.route('/admin/flag')
def admin_flag():
    client_ip = request.headers.get('X-Client-IP','')
    if client_ip != INTERNAL_IP:
        return "unauthorized", 403
    with open('/flag') as f:
        flag = f.read()
    return jsonify({"flag": flag})

@app.route('/internal/metadata')
def metadata():
    return jsonify({"instance-id":"i-ctf1234","secret":"do-not-use"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
