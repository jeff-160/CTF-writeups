import sqlite3
import os

conn = sqlite3.connect("fruits.db")
cur = conn.cursor()
secretname = os.urandom(32).hex()

cur.execute("""
CREATE TABLE IF NOT EXISTS gyul (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    grade INTEGER NOT NULL
);
""")

cur.execute(f"""
CREATE TABLE IF NOT EXISTS secretgyul (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    "{secretname}" TEXT NOT NULL,
    grade INTEGER NOT NULL
);
""")

cur.execute("INSERT INTO gyul (name, grade) VALUES ('orange', 2);")
cur.execute("INSERT INTO gyul (name, grade) VALUES ('gamgyul', 1);")
cur.execute("INSERT INTO gyul (name, grade) VALUES ('dekopon', 1);")
cur.execute(f"""
INSERT INTO secretgyul ("{secretname}", grade)
VALUES ('B1N4RY{{**redacted**}}', 1);
""")

conn.commit()
conn.close()

print("DB 설정 완료")
