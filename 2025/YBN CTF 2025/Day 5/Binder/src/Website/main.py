from flask import Flask, render_template,redirect, request, session, jsonify
from uuid import uuid4
import os
from jinja2 import Template
import json 
import requests 

BOT_URL = os.environ.get("BOT_URL","http://localhost:420/visit")
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY",os.urandom(32))

def to_bin(data):
    return ''.join(format(ord(char), '08b') for char in data)

def better_render_template(filename,dev_options={},context={}):
    with open(filename) as file:
        template = Template(file.read(),**dev_options)
    return render_template(template,**context)

def insert_details(uuid, username,description,dev_options = {}):
    DB_PATH = f"data/{uuid}.json"
    with open(DB_PATH, "w") as file:
        json.dump({
            "username":username,
            "description":description,
            "dev_options":dev_options
        },file)

def fetch_details(uuid):
    DB_PATH = f"data/{uuid}.json"
    if not os.path.exists(DB_PATH):
        return None
    with open(DB_PATH, "r") as file:
        data =json.load(file)
    return data

def create_user_page(uuid,username,description):
    with open("default_pages/user.html") as file:
        data = file.read()
    # Computers communicate in binary right???
    username_encoded = to_bin(username)
    description_encoded = to_bin(description)
    # Best way to block Template Injection
    data = data.replace("{username}",username_encoded)
    data = data.replace("{description}",description_encoded)
    directory = f"user_pages/{uuid}"
    file_path = f"{directory}/{username}"
    if os.path.exists(file_path):
        raise FileExistsError()
    os.makedirs(directory,exist_ok=True)
    with open(f"user_pages/{uuid}/{username}", "w") as file:
        file.write(data)

def delete_user_pages(uuid):
    directory = f"user_pages/{uuid}"
    os.makedirs(directory,exist_ok=True)
    pages = os.listdir(directory)
    for page in pages:
        file_path = os.path.join(directory,page)
        if os.path.isfile(file_path) and os.path.splitext(file_path)[1] == "":
            try:
                os.remove(file_path)
            except:
                print(f"Cannot remove {file_path}")

@app.before_request
def require_uuid():    
    if "uuid" not in session:
        session["uuid"] = str(uuid4())
    
@app.after_request
def set_secure_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'unsafe-inline';"
    return response
@app.route("/")
def index():
    return better_render_template("default_pages/index.html")

@app.route("/profile")
def profile():
    uuid = session["uuid"]
    user_data = fetch_details(uuid)
    if user_data is None:
        return redirect('/register')
    username,description,dev_options = user_data["username"],user_data["description"],user_data["dev_options"]
    if user_data is None:
        return better_render_template("default_pages/error.html",context={"error":"Create an Account First!"})
    return better_render_template(f"user_pages/{uuid}/{username}",dev_options)

@app.route("/register",methods=["POST","GET"])
def register():
    uuid = session["uuid"]
    if request.method == "GET":
        return better_render_template("default_pages/register.html")
    if request.method == "POST":
        description = request.form.get('description')
        username = request.form.get('username')
        dev_options = request.form.get("dev_options","{}")
        if dev_options:
            dev_options = json.loads(dev_options)
        if not username or not description:
            return better_render_template("default_pages/error.html",context={"error":"All fields are required!"})
        print(f"Registering user {username} with uuid {uuid}")        
        delete_user_pages(uuid)
        insert_details(uuid,username,description,dev_options)
        create_user_page(uuid,username,description)
        return redirect('/profile')

@app.route("/visit",methods=["POST"])
def visit():
    uuid = session["uuid"]
    requests.post(BOT_URL,data={
        "userId": str(uuid)
    })
    return better_render_template("default_pages/visit_requested.html")

@app.route("/admin")
def admin():
    userId = request.args.get("userId","")
    if not userId:
        return jsonify({"error":"No userId provided"}),400
    session['uuid'] = userId
    return jsonify({"success":True,"message":"Admin Bot Session Set"}),200
    
if __name__ == "__main__":
    app.run(port=5000, host = "0.0.0.0")
