from flask import Flask, render_template, session, request, make_response,redirect,url_for
import jwt
import sqlite3 
import uuid
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(64)
FLAG = os.getenv("FLAG","LNC25{TESTFLAG}")
def initialise_db():
    script = """
    CREATE TABLE IF NOT EXISTS kids (
    uuid TEXT NOT NULL,
    kid TEXT NOT NULL,
    secret TEXT,
    PRIMARY KEY (uuid)
    );
    """
    with connect() as db:
        db.executescript(script)
        db.commit()
    

def connect():
    conn = sqlite3.connect("kids.db")
    return conn

def get_kid(user_id, kid):
    with connect() as db:
        
        if kid is None: raise ValueError("kid Cannot be empty")
        result = db.execute(f'SELECT secret FROM kids WHERE uuid = "{user_id}" AND kid = "{kid}"')
        row = result.fetchone()
        if not row: raise ValueError("Invalid kid Provided")
        return row[0] if row else None

def create_secret(user_id):
    kid = str(uuid.uuid4())
    secret = secrets.token_hex(64)
    with connect() as db:
        db.execute(f'DELETE FROM kids WHERE uuid="{user_id}"')
        db.execute(f'INSERT INTO kids(uuid,kid,secret) VALUES ("{user_id}","{kid}","{secret}")')
        db.commit()
    return kid,secret

def check_jwt(user_id, jwt_token):
    try:
        header = jwt.get_unverified_header(jwt_token)
        if "kid" not in header:
            return False
        kid = header['kid']
        print(f"Kid: {kid}")
        secret = get_kid(user_id,kid)
        print(secret)
        payload = jwt.decode(jwt_token,secret, algorithms=["HS256"])
        return payload 
    except Exception as e:
        print(f"Error: {e}")
        return False

def generate_jwt(user_id,payload):
    kid,secret = create_secret(user_id)
    jwt_token = jwt.encode(payload,secret,algorithm="HS256",headers={
        "kid": kid
    })
    return kid,jwt_token

@app.before_request
def add_uuid():
    # ensures user has a valid uuid before every request
    if "uuid" not in session:
        session['uuid'] = str(uuid.uuid4())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_new_kid")
def new_kid():
    payload = {
        "role": "kid_owner"
    }
    user_id = session["uuid"]
    kid, jwt_token = generate_jwt(user_id,payload)
    resp = make_response(redirect(url_for("kid")))
    resp.set_cookie("jwt",jwt_token)
    return resp

@app.route("/get_kid", methods = ["GET"])
def kid():
    user_id = session["uuid"]
    if "jwt" in request.cookies:
        jwt_token = request.cookies.get("jwt")
        try:
            headers = jwt.get_unverified_header(jwt_token)
            if 'kid' in headers:
                return render_template("kids.html", kid = headers["kid"])
        except:
            pass
    payload = {
        "role": "kid_owner"
    }
    kid, jwt_token = generate_jwt(user_id,payload)
    resp = make_response(render_template("kids.html", kid = kid))
    resp.set_cookie("jwt",jwt_token)
    return resp
    
@app.route("/admin")
def admin():
    user_id = session["uuid"]
    if "jwt" not in request.cookies:
        return render_template("error.html", error = "No JWT token provided!")
    jwt_token = request.cookies.get("jwt")
    data = check_jwt(user_id,jwt_token)
    if not data:
        return render_template("error.html", error = "Invalid JWT!")
    role = data["role"]
    if role != "admin":
        return render_template("error.html", error = "You must be admin to view my kid stash :C")
    return render_template("admin.html", flag = FLAG)

if __name__ == "__main__":
    initialise_db()
    app.run(port = 5000, host="0.0.0.0")