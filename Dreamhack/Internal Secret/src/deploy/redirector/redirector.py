from flask import Flask, request, redirect, Response
from urllib.parse import unquote
app = Flask(__name__)
import requests

@app.route('/redir')
def redir():
    to = request.args.get('to','')
    if not to:
        return "provide ?to=", 400
    r = requests.get(to, headers={'X-Client-IP': '127.0.0.1'}, timeout=5)
    return Response(r.content, status=r.status_code, headers={'Content-Type': r.headers.get('Content-Type','text/plain')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
