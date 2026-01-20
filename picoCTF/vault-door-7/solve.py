x = [1096770097, 1952395366, 1600270708, 1601398833, 1716808014, 1734305081, 1681274424, 1700935729]

flag = ""
for num in x:
    b0 = (num >> 24) & 0xFF
    b1 = (num >> 16) & 0xFF
    b2 = (num >> 8) & 0xFF
    b3 = num & 0xFF
    flag += chr(b0) + chr(b1) + chr(b2) + chr(b3)

print("Flag: picoCTF{%s}" % flag)