from pwn import *
import re

io = remote("albo.ctf.pascalctf.it", 7004)

answers = ["Luca", "Rossi", "12/06/2011", "M", "Abano Terme"]

for ans in answers:
    io.sendlineafter(b':', ans.encode())

resp = io.recvall().decode()
io.close()

flag = re.findall(r'(pascalCTF{.+})', resp)[0]
print("Flag:", flag)