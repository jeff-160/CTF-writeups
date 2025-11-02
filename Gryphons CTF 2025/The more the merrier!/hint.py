# extract password from hint.txt

with open("hint.txt", "r") as f:
    content = [i for i in f.read().split("\n") if "Hint" in i]

s = ''

for line in content:
    if line[-1] == ' ':
        s += "0"
    else:
        s += "1"

print(s)
