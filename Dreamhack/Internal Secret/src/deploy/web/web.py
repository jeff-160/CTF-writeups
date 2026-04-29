from flask import Flask, request, jsonify
import requests, threading, uuid, time, sqlite3, os
from urllib.parse import urlparse, unquote

app = Flask(__name__)
JOB_DB = 'jobs.sqlite3'
ALLOWED_HOST = "example.com"
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN')
if not ADMIN_TOKEN:
    ADMIN_TOKEN = os.urandom(32).hex()

def init_db():
    if not os.path.exists(JOB_DB):
        conn = sqlite3.connect(JOB_DB)
        cur = conn.cursor()
        cur.execute("CREATE TABLE jobs (id TEXT PRIMARY KEY, url TEXT, status TEXT, result TEXT, created REAL)")
        cur.execute("CREATE TABLE audit (id INTEGER PRIMARY KEY AUTOINCREMENT, ev TEXT, job TEXT, info TEXT, t REAL)")
        conn.commit()
        conn.close()

def log_event(ev, job_id=None, info=None):
    conn = sqlite3.connect(JOB_DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO audit (ev, job, info, t) VALUES (?, ?, ?, ?)", (ev, job_id, info, time.time()))
    conn.commit()
    conn.close()

def host_allowed(parsed):
    host = parsed.hostname or ""
    return host == ALLOWED_HOST

def enqueue_job(url, client_ip):
    job_id = str(uuid.uuid4())
    conn = sqlite3.connect(JOB_DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO jobs (id, url, status, result, created) VALUES (?, ?, ?, ?, ?)",
                (job_id, url, 'queued', '', time.time()))
    conn.commit()
    conn.close()
    log_event('enqueue', job_id, f"url={url} ip={client_ip}")
    threading.Thread(target=worker_process, args=(job_id,)).start()
    return job_id

def worker_process(job_id):
    conn = sqlite3.connect(JOB_DB)
    cur = conn.cursor()
    cur.execute("SELECT url FROM jobs WHERE id=?", (job_id,))
    row = cur.fetchone()
    if not row:
        return
    url = row[0]
    log_event('worker_start', job_id, url)
    try:
        resp = requests.get(url, timeout=6, allow_redirects=True)
        snippet = resp.text[:1000].replace('\n',' ')
        result = f"code={resp.status_code} headers={dict(resp.headers)} body_snippet={snippet}"
        cur.execute("UPDATE jobs SET status=?, result=? WHERE id=?", ('done', result, job_id))
        conn.commit()
        log_event('worker_end', job_id, f"code={resp.status_code}")
    except Exception as e:
        cur.execute("UPDATE jobs SET status=?, result=? WHERE id=?", ('error', str(e), job_id))
        conn.commit()
        log_event('worker_error', job_id, str(e))
    finally:
        conn.close()

@app.route('/fetch', methods=['POST'])
def fetch():
    url = request.form.get('url', '').strip()
    client_ip = request.remote_addr
    if not url:
        return jsonify({"ok": False, "reason": "no url"}), 400
    try:
        parsed = urlparse(unquote(url))
    except Exception:
        return jsonify({"ok": False, "reason": "bad url"}), 400
    if not host_allowed(parsed):
        return jsonify({"ok": False, "reason": "host not allowed"}), 403
    job_id = enqueue_job(url, client_ip)
    return jsonify({"ok": True, "job_id": job_id}), 200

@app.route('/result/<job_id>')
def result(job_id):
    token = request.headers.get('X-Admin-Token') or request.headers.get('Admin-Token')
    client_ip = request.remote_addr

    if not token or token != ADMIN_TOKEN:
        log_event('admin_access_denied', job_id, f"ip={client_ip} token_ok=False")
        return jsonify({"ok": False, "reason": "forbidden"}), 403

    log_event('admin_access_granted', job_id, f"ip={client_ip} token_ok=True")

    conn = sqlite3.connect(JOB_DB)
    cur = conn.cursor()
    cur.execute("SELECT id, url, status, result, created FROM jobs WHERE id=?", (job_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return "no such job", 404
    return jsonify({"id": row[0], "url": row[1], "status": row[2], "result": row[3], "created": row[4]})

@app.route('/audit')
def audit():
    order = request.args.get('order', 'id').strip()
    if not order:
        return jsonify({"ok": False, "reason": "no order"}), 400
    if not order.startswith('id') and not order.startswith('t'):
        return jsonify({"ok": False, "reason": "no such order"}), 400
    conn = sqlite3.connect(JOB_DB)
    cur = conn.cursor()
    cur.execute(f"SELECT ev, job, info, t FROM audit ORDER BY {order} DESC LIMIT 80")
    rows = cur.fetchall()
    conn.close()
    events = []
    for r in rows[::-1]:
        events.append({"ev": r[0], "job": r[1], "info": r[2], "t": r[3]})
    return jsonify(events)

@app.route('/')
def index():
    return jsonify({"health": "good"})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)
