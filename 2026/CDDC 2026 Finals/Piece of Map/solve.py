with open('flag.txt', 'r') as f:
    flags = f.read().strip().split('\n')

for flag in flags:
    print(flag.replace(' ', '').replace('5', 'S'))