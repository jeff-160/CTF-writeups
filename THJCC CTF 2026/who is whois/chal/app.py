from flask import Flask, request, render_template_string
import subprocess, shlex
import pyotp
import base64

app = Flask(__name__)

INDEX_HTML = """
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <title>Whois 查詢</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: monospace; margin: 2rem; }
    form { margin-bottom: 1rem; }
    input[type=text]{ width: 36rem; max-width: 100%; padding: .5rem; }
    button{ padding: .5rem 1rem; }
    pre { white-space: pre-wrap; word-wrap: break-word; background:#f4f4f4; padding:1rem; border-radius:.5rem; }
    .argv{ color:#555; font-size:.9rem; }
  </style>
</head>
<body>
  <h1>Whois 查詢</h1>
  <form method="POST" action="/whois">
    <label>Domain name
      <input name="domain" type="text" placeholder="example.com" required>
    </label>
    <button type="submit">查詢</button>
  </form>
  {% if result is not none %}
    <h2>結果</h2>
    <pre>{{ result }}</pre>
  {% elif error is not none %}
    <h2>錯誤</h2>
    <pre>{{ error }}</pre>
  {% endif %}
</body>
</html>
"""
FLAG_VALUE = "THJCC{fake_flag_for_test}"
LOCAL_IPS = {"127.0.0.1", "::1"}

_ENC_SECRET = "Jl5cLlcsI10sKCYhLS40IykpMyQnIF8wIjEtPTM6OzI="
_XOR_KEY = "thjcc"

def _xor_decode(data: str, key: str) -> str:
    raw = base64.b64decode(data)
    return "".join(chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(raw))

def _get_totp_secret():
    return _xor_decode(_ENC_SECRET, _XOR_KEY)

def _deny(msg: str, code: int = 403):
    return (msg + "\n", code, {"Content-Type": "text/plain; charset=utf-8"})

@app.route("/", methods=["GET"])
def index():
    return render_template_string(INDEX_HTML, result=None, error=None, argv=None)

@app.route("/whois", methods=["POST"])
def whois_lookup():
    raw = request.form.get("domain", "").strip()
    if not raw:
        return render_template_string(INDEX_HTML, result=None, error="缺少參數", argv=None), 400

    try:
        args = ["whois"] + shlex.split(raw)
        proc = subprocess.run(args, capture_output=True, text=True, timeout=15)
    except subprocess.TimeoutExpired:
        return render_template_string(INDEX_HTML, result=None, error="查詢逾時", argv=" ".join(args)), 504
    except Exception as e:
        return render_template_string(INDEX_HTML, result=None, error=str(e), argv=" ".join(args) if 'args' in locals() else None), 500

    if proc.returncode != 0:
        return render_template_string(INDEX_HTML, result=None, error=proc.stderr or "whois 執行失敗", argv=" ".join(args)), 500

    return render_template_string(INDEX_HTML, result=proc.stdout, error=None, argv=" ".join(args))

@app.route("/flag", methods=["POST"])
def flag():
    if request.remote_addr not in LOCAL_IPS:
        return _deny("error: local only", 403)

    if request.headers.get("admin", "") != "thjcc":
        return _deny("error: missing/invalid admin header", 403)

    safekey = request.form.get("safekey", "").strip()
    if not safekey:
        return _deny("error: missing safekey", 400)

    totp = pyotp.TOTP(_get_totp_secret())
    if not totp.verify(safekey):
        return _deny("error: invalid totp", 403)

    return (FLAG_VALUE + "\n", 200, {"Content-Type": "text/plain; charset=utf-8"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=13316)
