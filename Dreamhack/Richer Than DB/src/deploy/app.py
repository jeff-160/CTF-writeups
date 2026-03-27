from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import os
from functools import wraps
from mysql import db

app = Flask(__name__)

app.secret_key = os.urandom(24)

@app.route('/admin', methods=['POST'])
def admin():
    if request.method == 'POST':
        c = request.form.get('c')
        if c == "1": #init db
            cursor = db.cursor()
            new_table_name = request.form.get('new_table_name')
            new_table_option = request.form.get('new_table_option')
            only_alphanumeric_and_equal = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_=")
            if not set(new_table_name).issubset(only_alphanumeric_and_equal):
                cursor.close()
                return "Table name can only contain alphanumeric characters and equal sign!"
            if new_table_option != "":
                if not set(new_table_option).issubset(only_alphanumeric_and_equal):
                    cursor.close()
                    return "Table option can only contain alphanumeric characters and equal sign!"
            cursor.execute("DROP TABLE IF EXISTS users")
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {new_table_name} (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), money BIGINT DEFAULT 0) {new_table_option};") 
            db.commit()
            cursor.close()
            return "Init db success!"
        elif c == "2": #show db
            cursor = db.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            cursor.close()
            return str(tables)
        elif c == "3": #show users
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            cursor.close()
            return str(users)
        elif c == "4": #delete user
            cursor = db.cursor()
            username = request.form.get('username')
            cursor.execute("DELETE FROM users WHERE username=%s", (username,))
            db.commit()
            cursor.close()
            return "Delete user success!"
        return "Invalid command!"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session.clear()
        username1 = request.form.get('username1')
        username2 = request.form.get('username2')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        money1 = request.form.get('money1')
        money2 = request.form.get('money2')
        
        try:
            if int(money1) < 0 or int(money2) < 0:
                return render_template('register.html', msg="Money must be positive!")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s OR username=%s", (username1, username2))
            user = cursor.fetchone()
            if user:
                return render_template('register.html', msg="Username already exists!")
            cursor.execute("INSERT INTO users (username, password, money) VALUES (%s, %s, %s), (%s, %s, %s)", (username1, password1, money1, username2, password2, money2))
            cursor.execute("SELECT * FROM users WHERE username=%s", (username1,))
            user1 = cursor.fetchone()
            cursor.execute("SELECT * FROM users WHERE username=%s", (username2,))
            user2 = cursor.fetchone()
            print(user1)
            print(user2)
            if user1[3] != user2[3]: #check if money1 and money2 is same
                return render_template('register.html', msg="Money is not same!")
            db.commit()
            cursor.close()
            session["money"] = int(money1) + int(money2)
            return render_template('register.html', msg="Register success!")
        
        except Exception as e:
            return render_template('register.html', msg=f"Error: {str(e)}")
    return render_template('register.html')

@app.route('/flag')
def flag():
    if session.get("money") == 18446744073709551734:
        return "Layer7{NOTFLAG}"
    return "You are not rich enough!"
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)