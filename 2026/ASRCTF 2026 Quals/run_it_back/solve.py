ALPHA = "abcdefghijklmnopqrstuvwxyz0123456789_"
M = 37

KEY = [31, 29, 0, 6, 11, 3, 30, 19, 31, 5, 15, 5, 24, 20, 30, 30, 23, 4, 31, 32, 13, 31, 25]
n = len(KEY)

# Build matrix A where A v = KEY (mod 37)
A = [[0]*n for _ in range(n)]

for i in range(n):
    A[i][i] = 1
    A[i][(i-1) % n] = (-11) % M
    A[i][(i+1) % n] = (-7) % M

def modinv(a, m):
    return pow(a, -1, m)

# Gaussian elimination mod M
for i in range(n):
    # find pivot
    for r in range(i, n):
        if A[r][i] % M != 0:
            A[i], A[r] = A[r], A[i]
            KEY[i], KEY[r] = KEY[r], KEY[i]
            break

    inv = modinv(A[i][i] % M, M)

    # normalize row
    for j in range(i, n):
        A[i][j] = (A[i][j] * inv) % M
    KEY[i] = (KEY[i] * inv) % M

    # eliminate others
    for r in range(n):
        if r != i:
            factor = A[r][i]
            for j in range(i, n):
                A[r][j] = (A[r][j] - factor * A[i][j]) % M
            KEY[r] = (KEY[r] - factor * KEY[i]) % M

# extract solution
v = KEY

flag = "".join(ALPHA[x] for x in v)
print("ASRCTF{" + flag + "}")