# app.py
import os
from datetime import datetime
import secrets

from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash

from db import (
    db_get_user_by_username,
    db_create_user,
    db_update_user_password,
    db_create_reset_token,
    db_get_valid_token,
    db_mark_token_used,
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(32))

TOKEN_TTL_MINUTES = int(os.getenv("TOKEN_TTL_MINUTES", "30"))

users = {}
inbox = {u: [] for u in users}
password_reset_tokens_v1 = {}

def inbox_post(username: str, text: str):
    inbox.setdefault(username, []).append({
        "text": text,
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    })

try:
    init_accounts = {
        'admin': os.urandom(32).hex(),
        'guest': 'guest',
    }
    for id, pw in init_accounts.items():
        users[id] = generate_password_hash(pw)

    with open('./flag.txt', 'r') as f:
        inbox_post('admin', f.readline())
except Exception as e:
    print(f"[WARN] startup failed: {e}")
    

def require_login():
    if "user" not in session:
        flash("Please log in first.", "error")
        return False
    return True


@app.route("/v1/")
def home_v1():
    return render_template("home.html")

@app.route("/v1/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username in users and check_password_hash(users[username], password):
            session["user"] = username
            inbox.setdefault(username, [])
            flash("Logged in successfully.", "success")
            return redirect(url_for("home"))
        flash("Invalid username or password.", "error")
    return render_template("login.html")

@app.route("/v1/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Username and password are required.", "error")
        elif username in users:
            flash("Username already exists.", "error")
        else:
            users[username] = generate_password_hash(password)
            inbox.setdefault(username, [])
            flash("Account created! You can now log in.", "success")
            return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/v1/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

@app.route("/v1/mypage")
def mypage():
    if not require_login():
        return redirect(url_for("login"))
    username = session["user"]
    messages = inbox.get(username, [])
    return render_template("mypage.html", messages=messages, username=username)

@app.route("/v1/request-password-change", methods=["GET", "POST"])
def request_password_change():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if username in users:
            token = secrets.token_urlsafe(16)
            password_reset_tokens_v1[token] = username
            reset_path = url_for("password_reset", token=token)
            inbox_post(username, f"Password change link: {reset_path} (one-time use)")
        flash("If the username exists, a password change link was delivered to their My Page.", "info")
        return redirect(url_for("login"))
    return render_template("password_request.html")

@app.route("/v1/change-password/<token>", methods=["GET", "POST"])
def password_reset(token):
    if token not in password_reset_tokens_v1:
        flash("Invalid or expired link.", "error")
        return redirect(url_for("home"))

    username = password_reset_tokens_v1[token]
    if request.method == "POST":
        new_pw = request.form.get("new_password", "")
        confirm_pw = request.form.get("confirm_password", "")
        if not new_pw or not confirm_pw:
            flash("Please fill out both fields.", "error")
            return render_template("password_reset.html", token=token, username=username)
        if new_pw != confirm_pw:
            flash("New password and confirmation do not match.", "error")
            return render_template("password_reset.html", token=token, username=username)

        users[username] = generate_password_hash(new_pw)
        del password_reset_tokens_v1[token]
        flash("Password updated successfully. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("password_reset.html", token=token, username=username)

@app.route("/v2/")
def home_v2():
    return render_template("home.html")

@app.route("/v2/login", methods=["POST"])
def login_v2():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        row = db_get_user_by_username(username)
        if row and check_password_hash(row["password_hash"], password):
            session["user"] = row["username"]
            inbox.setdefault(row["username"], [])
            flash("Logged in successfully.", "success")
            return redirect(url_for("home_v2"))

        flash("Invalid username or password.", "error")
    return render_template("login.html")

@app.route("/v2/signup", methods=["POST"])
def signup_v2():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password are required.", "error")
        elif db_get_user_by_username(username):
            flash("Username already exists.", "error")
        else:
            db_create_user(username, password)
            inbox.setdefault(username, [])
            flash("Account created! You can now log in.", "success")
            return redirect(url_for("login_v2"))

    return render_template("signup.html")

@app.route("/v2/logout")
def logout_v2():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("home_v2"))

@app.route("/v2/mypage")
def mypage_v2():
    if not require_login():
        return redirect(url_for("login_v2"))
    username = session["user"]
    messages = inbox.get(username, [])
    return render_template("mypage.html", messages=messages, username=username)

@app.route("/v2/request-password-change", methods=["POST"])
def request_password_change_v2():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if db_get_user_by_username(username):
            try:
                token = db_create_reset_token(username=db_get_user_by_username(username)['username'], ttl_minutes=TOKEN_TTL_MINUTES)
                reset_path = url_for("password_reset_v2", token=token)
                inbox_post(username, f"Password change link: {reset_path} (one-time use)")
            except Exception as e:
                print(f"[ERROR] DB token create failed: {e}")
                flash("Service temporarily unavailable. Please try again later.", "error")
                return redirect(url_for("login_v2"))
    abort(501)

@app.route("/v2/change-password/<token>", methods=["POST"])
def password_reset_v2(token):
    try:
        row = db_get_valid_token(token)
    except Exception as e:
        print(f"[ERROR] DB token read failed: {e}")
        row = None

    if not row:
        abort(501)

    username = row["username"]
    if request.method == "POST":
        new_pw = request.form.get("new_password", "")
        confirm_pw = request.form.get("confirm_password", "")
        if not new_pw or not confirm_pw:
            abort(501)
        if new_pw != confirm_pw:
            abort(501)

        db_update_user_password(username, new_pw)
        try:
            db_mark_token_used(row["id"])
        except Exception as e:
            print(f"[WARN] Could not mark token used: {e}")

    abort(501)

@app.route("/")
def home():
    return redirect(url_for("home_v1"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
