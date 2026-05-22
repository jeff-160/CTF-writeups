from connections import connect_mysql
from threading import RLock
from hashlib import sha256

lock = RLock()
db, cursor = connect_mysql()


def add_user(id, pw):
    sha256_pw = sha256(pw.encode()).hexdigest()
    try:
        query = "INSERT INTO users (id, pw) VALUES (%s, %s)"
        with lock:
            cursor.execute(query, (id, sha256_pw))
            db.commit()

    except Exception as e:
        print(f"[-] db Error : {e}")
        db.rollback()
        db.close()


def get_user_by_id(id):
    try:
        query = "SELECT id FROM users WHERE id=%s"
        with lock:
            cursor.execute(query, (id))
            user = cursor.fetchone()
            if user:
                return user

    except Exception as e:
        print(f"[-] db Error : {e}")
        db.close()


def get_user_by_id_and_pw(id, pw):
    sha256_pw = sha256(pw.encode()).hexdigest()
    try:
        query = "SELECT * FROM users WHERE id=%s and pw=%s"
        with lock:
            cursor.execute(query, (id, sha256_pw))
            user = cursor.fetchone()
            if user:
                return user
    except Exception as e:
        print(f"[-] db Error : {e}")
        db.close()


def get_bread_by_name(bread_name):
    try:
        query = "SELECT name FROM breads WHERE name LIKE %s"
        with lock:
            cursor.execute(query, (bread_name + "%"))
            user = cursor.fetchone()
            if user:
                return user

    except Exception as e:
        print(f"[-] db Error : {e}")
        db.close()
