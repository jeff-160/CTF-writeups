from pwn import *

while True:
  r = remote("fortune-cookie.challenges.2025.vuwctf.com", 17)

  res = r.recvline().decode()
  
  if "flag" in res or "Vuw" in res:
    print(res)
    exit()

  r.close()