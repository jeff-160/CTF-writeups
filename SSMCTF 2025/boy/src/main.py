from string import printable
from flask import Flask, request, render_template, send_file, redirect, url_for, flash
import sqlite3
import os
from secret import flag

def init_db():
    with sqlite3.connect('boy.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS duh (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        boy TEXT,
                        duhhh TEXT)''')

        conn.execute('''CREATE TABLE IF NOT EXISTS flag (
                        flagtext TEXT)''')
        
        duh = [("duh", "duh!"), ("yeah", "yeah!"), ("lol", "lol!")]
        conn.executemany('''INSERT INTO duh (boy, duhhh) VALUES (?, ?)''', duh)
        conn.execute('''INSERT INTO flag (flagtext) VALUES (?)''', (flag,))

init_db()
def search(boy):
    try: 
        with sqlite3.connect('boy.db') as conn:
            # does this work? duh it does...
            blacklist = (char for char in printable if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnoprqstuvwxyz")

            if 'flag' in boy: return "nope!"
            
            filtered_term = ''
            for char in boy:
                if char not in blacklist:
                    filtered_term += char

            cursor = conn.cursor()
            query = f"SELECT duhhh FROM duh WHERE boy = '{filtered_term}'"
            cursor.execute(query)
            result = cursor.fetchone()

            if result is None: result = "duh :/" 
            else: 
                result = result[0]
                if "SSMCTF" in result: return "nope!"
        
            return result
    except Exception as e:
        return str(e)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        duh = request.form['duh']
        return render_template('base.html', duh=search(duh))
    return render_template('base.html', duh='duh')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)