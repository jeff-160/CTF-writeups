import sys

s = sys.argv[1]

r = [f'({ord(c) - 87}).toString(36)' for c in s]

print(",".join(r))