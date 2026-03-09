import sqlite3
import os

USER_DATABASE = 'data/users.db'
MEMO_DATABASE = 'memos.db'

def init_db():
    user_conn = sqlite3.connect(USER_DATABASE)
    user_c = user_conn.cursor()

    user_c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL,
                      role TEXT DEFAULT 'user')''')

    user_conn.commit()
    user_conn.close()

    memo_conn = sqlite3.connect(MEMO_DATABASE)
    memo_c = memo_conn.cursor()

    memo_c.execute('''CREATE TABLE IF NOT EXISTS memos
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      title TEXT NOT NULL,
                      content TEXT NOT NULL,
                      template TEXT DEFAULT 'default')''')

    memo_conn.commit()
    memo_conn.close()

def get_user_db_connection():
    conn = sqlite3.connect(USER_DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_memo_db_connection():
    conn = sqlite3.connect(MEMO_DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
