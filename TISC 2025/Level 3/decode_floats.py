import struct

with open("cuboid.txt", "r") as f:
    data = f.read().split("\n")

enc = []

for line in data:
    segments = map(lambda x: x[1:], line.split(" ")[1:])

    enc.extend(segments)

raw_bytes = b''.join(struct.pack("<f", float(n)) for n in enc)

decoded = raw_bytes.decode("utf-16-le")

print(decoded)