a = 2401941830
result = (3 * a) & 0xffffffff

print("Flag: picoCTF{%s}" % hex(result)[2:])