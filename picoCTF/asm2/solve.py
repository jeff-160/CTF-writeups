def asm2(y, x):
    while y <= 0xd72d:
        x += 1
        y += 0xcb
    return x

print("Flag:", hex(asm2(0xf, 0x17)))