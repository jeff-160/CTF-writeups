with open("crazy.txt", 'r') as f:
    contents = [line.strip() for line in f.read().split('\n') if len(line)]

flag = ''

for line in contents:
    flag += line.split(' ')[-2]

print("Flag:", flag[::-1])