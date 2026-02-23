from pwn import *
import re

r = remote("tcp.ybn.sg", 18339)

with open('answers.txt', 'r') as f:
    answers = f.read().strip().split('\n')

for answer in answers:
    r.sendlineafter(b'>', answer.encode())

resp = r.recvall().decode()
r.close()

flag = re.findall(r'(YBN{.+})', resp)[0]
print("Flag:", flag)