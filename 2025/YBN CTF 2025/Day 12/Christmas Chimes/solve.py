with open("bin.txt", 'r') as f:
    chunks = f.read().replace("\n", " ").strip().split(" ")

chunks = [c for c in chunks if len(c)]

morse = ''.join(chr(int(chunk, 2)) for chunk in chunks).replace("jingle", '.').replace("bell", '-')

print('\n'.join([l.strip() for l in morse.split('/')]))