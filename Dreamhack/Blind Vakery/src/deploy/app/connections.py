import pymysql


def connect_mysql():
    db = pymysql.connect(
        host="localhost",
        port=3306,
        user="vakery_user",
        passwd="vakery_password",
        db="vakery_db",
        charset="utf8",
    )
    cursor = db.cursor()
    return db, cursor
