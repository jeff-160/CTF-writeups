#!/usr/bin/python
from pyfiglet import Figlet
import ast
import string
import sys
import os
import _frozen_importlib

def verify(m):
    allowed = set(string.ascii_lowercase+'()[]: ._@\n'+string.digits)
    if allowed | set(code) != allowed:
        print("ERROR: not allowed <ascii>")
        return False
    
    for i in ast.walk(m):
        match type(i):
            case (ast.Import|ast.ImportFrom|ast.Call):
                print(f"ERROR: Banned statement {i}")
                return False
    return True

code=''
f=Figlet()
print(f.renderText('* * * * * * * * * *'))
print(f.renderText('             BISC CTF\n                Python\n         JailBreak!!!'))
print(f.renderText('* * * * * * * * * *'))
print("code:")
while True:
  line = sys.stdin.readline()
  if line.startswith("end"):
    break
  code += line

bisc=compile(code,"",'exec',flags=ast.PyCF_ONLY_AST)

if verify(bisc):
    compiled=compile(code,"",'exec')
    try:
        exec(compiled,{'__builtins__':None, '__loader__':_frozen_importlib.BuiltinImporter})
    except Exception as e:
        print(f"ERROR: Exception <{e}>")
