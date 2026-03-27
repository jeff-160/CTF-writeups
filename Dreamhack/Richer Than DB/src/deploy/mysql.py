import pymysql
import os

HOST = os.getenv("MYSQL_HOST")
USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
DB = os.getenv("MYSQL_DATABASE")

while True:
    try:
        print(f"Connecting to MySQL database at {HOST}")
        db = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB,
            charset="utf8",
        )
        break
    except pymysql.err.OperationalError:
        print("Failed to connect to MySQL database. Retrying...")
        continue

print("Connected to MySQL database")

cursor = db.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), money BIGINT DEFAULT 0);"
)
db.commit()
cursor.close()