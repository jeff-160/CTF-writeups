data = open("output.txt").read()

rows = data.split("}")

rows = [r for r in rows if r and r != "~"]

top = []
bot = []

for r in rows:
    t=""
    b=""
    for ch in r:
        v = ord(ch)-32
        bits = format(v,'06b')
        t += bits[:3]
        b += bits[3:]
    top.append(t)
    bot.append(b)

orig = []
for i in range(len(top)):
    orig.append(top[i])
    orig.append(bot[i])

flag = '\n'.join("".join("#" if c=="1" else " " for c in row) for row in orig)

with open("flag.txt", 'w') as f:
    f.write(flag)