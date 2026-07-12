import subprocess
import os

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

def query(sql):
    data = []
    result = None

    try:
        result = subprocess.check_output(["mariadb", "-h" + DB_HOST, "-u" + DB_USER, "-p" + DB_PASSWORD, "-e", sql, "--batch", "--ssl=0", DB_NAME])
    except subprocess.CalledProcessError as e:
        raise Exception("Failed to execute query")

    result = result.decode("utf-8").splitlines()
    if len(result) == 0:
        return []
    
    columns = result[0].split("\t")
    
    for row in result[1:]:
        row = row.split("\t")
        if len(row) != len(columns):
            raise Exception("Invalid row")
        data.append({columns[i]: row[i] for i in range(len(columns))})
    
    return data
