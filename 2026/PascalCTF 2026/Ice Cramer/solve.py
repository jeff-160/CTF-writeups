import re
import numpy as np

def parse_equations(raw):
    equations = []
    rhs = []

    lines = raw.split('\n')

    vars_found = re.findall(r"x_(\d+)", lines[0])
    n = max(map(int, vars_found)) + 1

    for line in lines:
        coeffs = [0] * n

        left, right = line.split("=")
        right = int(right.strip())

        terms = left.split("+")
        for term in terms:
            term = term.strip()
            k, x = term.split("*")
            idx = int(x.replace("x_", ""))
            coeffs[idx] = int(k)

        equations.append(coeffs)
        rhs.append(right)

    return np.array(equations, dtype=float), np.array(rhs, dtype=float)

from pwn import *

io = remote('cramer.ctf.pascalctf.it', 5002)

equations = io.recvuntil(b'Solve', drop=True).decode().strip()
io.close()

A, b = parse_equations(equations)

solution = np.linalg.solve(A, b)

flag_chars = [chr(int(round(x))) for x in solution]
flag = "pascalCTF{" + "".join(flag_chars) + "}"

print("Flag:", flag)