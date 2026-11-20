from flask import Flask, request, render_template, redirect, url_for, abort, request, jsonify
import os
import re
import requests
import ipaddress
import subprocess

app = Flask(__name__)
app.secret_key = os.urandom(64)

info_value = ''


@app.route('/')
def index():
    return redirect(url_for('info'))


@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        global info_value
        info_value = request.form.get('info_value', '')
        return redirect(url_for('info'))

    ip_address = request.remote_addr
    ip_obj = ipaddress.ip_address(ip_address)

    if ip_obj.is_private or ip_obj.is_loopback:
        FLAG = open('/flag', 'r').read()
        value = FLAG
    else:
        value = ''

    return render_template('post.html', value=value)


@app.route('/info', methods=['GET'])
def info():
    global info_value
    return render_template('info.html', info_value=info_value)


@app.route('/callback', methods=['GET'])
def callback():
    ip_address = request.remote_addr
    ip_obj = ipaddress.ip_address(ip_address)

    if not (ip_obj.is_private or ip_obj.is_loopback):
        abort(403, 'Access denied')

    callback_fn = request.args.get('callback', 'console.log')
    if not re.fullmatch(r'[A-Za-z0-9.]+', callback_fn):
        abort(400, 'Invalid callback parameter')

    global info_value
    return render_template('callback.html', callback_fn=callback_fn, info_value=info_value)


@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        report_url = request.form.get('report_url', '')
        resp = requests.post('http://user:31337/visit', json={'url': report_url})
        if resp.ok:
            return render_template('report.html', submitted=True)
    return render_template('report.html', submitted=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
