ciphertext = r"VLu\\8m9Xl(>W{_?TD[q \202\033\213P\200F~\025\212W}ZPT\201Q\214\f\224D"
flag = ciphertext.encode("latin1").decode("unicode_escape").encode("latin1")

inp = bytearray(40)

for i, b in enumerate(flag):
    if i % 2 == 0:
        inp[i] = (b - i) & 0xff
    else:
        inp[i] = (b + i) & 0xff

print("Flag: pascalCTF{%s}" % inp.decode())