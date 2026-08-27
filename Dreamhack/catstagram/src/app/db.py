import sqlite3
import secrets
import os
import json

ADMIN_PASSWORD = secrets.token_hex(20)
print(f"Admin password: {ADMIN_PASSWORD}")

def get_db_conn():
    conn = sqlite3.connect("database.db")
    return conn

def init_db():
    os.system("rm database.db")
    conn = get_db_conn()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user' CHECK(role IN ('admin', 'user'))
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        owner TEXT NOT NULL,
        description TEXT NOT NULL,
        url TEXT NOT NULL,
        like INTEGER NOT NULL 
    )
    """)
    
    cursor.execute("insert into users(username, password, role) values (?, ?, ?)", ('admin', ADMIN_PASSWORD, 'admin'))
    cursor.execute("insert into users(username, password, role) values (?, ?, ?)", ('winky', '12345678', 'user'))
    cats = json.load(open('cats.json'))
    cats = [(i['name'], i['owner'], i['description'], i['url']) for i in cats]
    cursor.executemany(f"insert into cats(name, owner, description, url, like) values (?, ?, ?, ?, 0)", cats)
    conn.commit()
    conn.close()
    
def add_user(username, password):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(f'insert into users(username, password) values (?, ?)', (username, password))
    conn.commit()
    conn.close()
    
def is_user_exists(username):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(f'select * from users where username = ?', (username, ))
    result = cursor.fetchone()
    conn.close()
    return result is not None
    
def get_cats():
    conn = get_db_conn()
    cursor = conn.cursor()
    result = cursor.execute("select * from cats")
    return result.fetchall()
    
def like_cat(cat_id):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("update cats set like=like+1 where id = ?", (cat_id, ))
    cursor.execute("select like from cats where id = ?", (cat_id, ))
    new_like_count = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return new_like_count

def authenticate_user(username, password):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('select * from users where username = ? and password = ?', (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_cat_post(name, owner, description, filename):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('insert into cats(name, owner, description, url, like) values (?, ?, ?, ?, 0)', 
                   (name, owner, description, filename))
    conn.commit()
    conn.close()

def is_filename_exists(filename):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('select * from cats where url = ?', (filename,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_user_role(username):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('select role from users where username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None