from pwn import *
import re

# get function names
elf = ELF('./my_secret_recipe')
funcs = [name.replace("got.", "") for name, _ in elf.symbols.items() if "got" in name and "_" not in name]

with open('out.txt', 'r') as f:
    lines = f.read().split('\n')

# heuristic extraction from disassembly
flag = ""

for func in funcs:
    try:
        idx = [i for i in range(len(lines)) if func in lines[i]][0] + 3
        char = re.findall(r'mov(.+),', lines[idx])[0].strip()[1:]
        
        flag += chr(int(char, 16))
    except:
        ...

print("Flag:", flag)