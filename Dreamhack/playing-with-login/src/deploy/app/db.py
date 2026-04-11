# db.py
import os
import secrets
from datetime import datetime, timedelta

import pymysql
from pymysql.cursors import DictCursor
from werkzeug.security import generate_password_hash

DB_HOST = os.getenv("DB_HOST", "db")
# DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "flask_service")

def get_db():
    return pymysql.connect(
        host=DB_HOST,
        # port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        autocommit=True,
        cursorclass=DictCursor,
    )

def db_get_user_by_username(username: str):
    con = get_db()
    try:
        with con.cursor() as cur:
            cur.execute(
                "SELECT id, username, password_hash FROM users WHERE username=%s",
                (username,),
            )
            return cur.fetchone()
    finally:
        con.close()

def db_create_user(username: str, password: str):
    con = get_db()
    try:
        with con.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, generate_password_hash(password)),
            )
            return cur.lastrowid
    finally:
        con.close()

def db_update_user_password(username: str, new_password: str):
    con = get_db()
    try:
        with con.cursor() as cur:
            cur.execute(
                "UPDATE users SET password_hash=%s WHERE username=%s",
                (generate_password_hash(new_password), username),
            )
    finally:
        con.close()

def db_create_reset_token(username: str, ttl_minutes: int) -> str:
    token = secrets.token_urlsafe(24)
    expires_at = datetime.utcnow() + timedelta(minutes=ttl_minutes)
    con = get_db()
    try:
        with con.cursor() as cur:
            cur.execute(
                "INSERT INTO password_reset_tokens (username, token, expires_at) VALUES (%s, %s, %s)",
                (username, token, expires_at),
            )
    finally:
        con.close()
    return token

def db_get_valid_token(token: str):
    con = get_db()
    try:
        with con.cursor() as cur:
            cur.execute(
                "SELECT id, username, token, expires_at, used FROM password_reset_tokens WHERE token=%s",
                (token,),
            )
            row = cur.fetchone()
            if not row:
                return None
            if row["used"]:
                return None
            if datetime.utcnow() > row["expires_at"]:
                return None
            return row
    finally:
        con.close()

def db_mark_token_used(token_id: int):
    con = get_db()
    try:
        with con.cursor() as cur:
            cur.execute("UPDATE password_reset_tokens SET used=1 WHERE id=%s", (token_id,))
    finally:
        con.close()
