from pwn import *
import re

r = remote("tcp.ybn.sg", 11833)

with open("answers.txt", "r") as f:
    lines = f.read().strip().split('\n')

for qn, line in enumerate(lines, start=1):
    r.sendlineafter(b">", line.encode())

resp = r.recvall().decode()
r.close()

flag = re.findall(r'(YBN{.+})', resp)[0]
print("Flag:", flag)