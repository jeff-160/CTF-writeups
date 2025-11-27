def get_hex(raw):
    enc = []
    i = 0
    
    while i < len(raw):
        if raw[i] == "\\":
            enc.append(raw[i + 1 : i + 1 + 2])
            i += 3
        else:
            enc.append(format(ord(raw[i]), '02x'))
            i += 1
    
    return [int(b, 16) for b in enc]

enc = bytes(get_hex(r"\18j|a\118i7[H~Jh^Ko\1f]\5cw4kP\15pO?\5cEo\14\06\05}>=\04\16.\12L\00\00")[:-2])

n = len(enc)
y = list(enc)

for i in range(0, n - 1, 2):
    y[i], y[i + 1] = y[i + 1], y[i]

orig = [0] * n

for i in range(n):
    val = y[i]
    val ^= [7, 6, 5][i % 3]
    val ^= 9 if (i % 2 == 0) else 8
    val ^= (i % 10)
    
    if i > 2:
        val ^= y[i - 3]
    
    if i > 0:
        val ^= y[i - 1]
    
    val ^= 20
    orig[i] = val

print(bytes(orig).decode())