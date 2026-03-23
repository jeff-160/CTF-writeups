from pwn import *

io = remote("streams.tamuctf.com", 443, ssl=True, sni="decreasing")
io.interactive(prompt="")
