#!/usr/bin/env python3
import ast,sys,string,_frozen_importlib

ALLOWED=set(string.ascii_lowercase+string.digits+'()[]: ._@\n')
BANNED=(ast.Import,ast.ImportFrom,ast.Call,ast.If,ast.Try,ast.While,ast.For,ast.Return,ast.Pass)

def verify(tree, s):
    if not isinstance(s,str):
        print('error:type str');return False
    bad=set(s)-ALLOWED
    if bad:
        print('error:charset',''.join(sorted(bad)));return False
    stack=[]
    for c in s:
        if c=='[': stack.append(0)
        elif c==']':
            if not stack: print('error:brackets ]');return False
            stack.pop()
        elif c==':' and stack:
            stack[-1]+=1
            if stack[-1]>1: print('error:slice :>1');return False
    if stack:
        print('error:brackets [');return False
    for n in ast.walk(tree):
        if isinstance(n, BANNED):
            print(f'error:ast banned {type(n).__name__}')
            return False
    return True

print("""𝔞𝔰𝔱 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⣴⣄⠀⠀⠀⠀⠀  ⢀⡄
‾‾‾⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡾⣷⢿⡀⠀⠀⠀⠀⣠⣾⣿⣿⡄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣦⣴⣿⡋⠀⠀⠈⢳⡄⠀⢠⣾⡟⠁⠈⢿⣿⡄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⠿⠛⠉⠉⠁⠀⠀⠀⠹⡄⣿⣿⠁   ⢹⣿⡄
⠀⠀⠀⠀⠀⣠⣾⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⣰⣏⢻⣿⡆⠁ ⠁ ⣿⡇⠀⠀⠀
⠀⠀⠀⢀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣆⠹⣷    ⢹⣧⡀⠀⠀⠀
⠀⠀⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⠋⠉⠛⠂⠹⠿⡄  ⣼⣿⣧⠀⠀
⠀⢠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣿⣿⣿⣷⣾⣿⡇⢀⠀⣼⣷⣼⣿⣿⣿⣧⠀
⠰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⡘⢿⣿⣿⣿⣿⣿⠀
⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣷⡈⠿⢿⣿⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠁⢙⠛⣿⣿⣿⣿⡟⠀⡿⠀⠀⢀⣿⣿⡇
⠀            ⠀⠀⠀⠸⣶⣤⣉⣛⠻⠇⢠⣿⣾⣿⡄⢻⣿⠁
\033[4mend\033[0m to send.     ⠸⣿⣿⣿⣦⣤⣾⣿⣿⣿⣿⣆⠁
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾""")

buf=[]
for line in sys.stdin:
    if line.startswith('end'): break
    buf.append(line)
src=''.join(buf)
tree=compile(src,'','exec',flags=ast.PyCF_ONLY_AST)
if verify(tree, src):
    exec(compile(src,'','exec'),
         {'__builtins__':{},
          '__loader__':_frozen_importlib.BuiltinImporter})