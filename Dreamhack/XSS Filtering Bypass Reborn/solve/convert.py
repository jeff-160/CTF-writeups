with open("payload.js", "r", encoding='utf-8') as f:
    payload = f.read().strip()

payload = payload.replace("!![]", "(+[]==+[])").replace("![]", "([]==[])")

print(payload)