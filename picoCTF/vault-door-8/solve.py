def switch_bits(c, p1, p2):
    mask1 = 1 << p1
    mask2 = 1 << p2

    bit1 = c & mask1
    bit2 = c & mask2
    rest = c & ~(mask1 | mask2)

    shift = p2 - p1
    return ((bit1 << shift) | (bit2 >> shift) | rest) & 0xFF

def unscramble_byte(c):
    c = switch_bits(c, 6, 7)
    c = switch_bits(c, 2, 5)
    c = switch_bits(c, 3, 4)
    c = switch_bits(c, 0, 1)
    c = switch_bits(c, 4, 7)
    c = switch_bits(c, 5, 6)
    c = switch_bits(c, 0, 3)
    c = switch_bits(c, 1, 2)
    return c

expected = [
    0xF4, 0xC0, 0x97, 0xF0, 0x77, 0x97, 0xC0, 0xE4,
    0xF0, 0x77, 0xA4, 0xD0, 0xC5, 0x77, 0xF4, 0x86,
    0xD0, 0xA5, 0x45, 0x96, 0x27, 0xB5, 0x77, 0xF1,
    0xC2, 0xD2, 0x95, 0xD0, 0xF0, 0x94, 0xF1, 0x95
]

flag = ''.join(chr(unscramble_byte(c)) for c in expected)
print("Flag: picoCTF{%s}" % flag)