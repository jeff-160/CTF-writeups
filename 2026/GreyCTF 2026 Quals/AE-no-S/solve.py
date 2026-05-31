#!/usr/bin/env python3
import json

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def bytes_to_bits(b):
    bits = []
    for byte in b:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def bits_to_bytes(bits):
    result = []
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        result.append(byte)
    return bytes(result)

def solve_block(target_ct, zero_ct, cols):
    n = 128
    target_bits = bytes_to_bits(xor_bytes(target_ct, zero_ct))

    matrix = []
    for row in range(n):
        mat_row = [cols[j][row] for j in range(n)]
        mat_row.append(target_bits[row])
        matrix.append(mat_row)

    # Gaussian elimination over GF(2)
    pivot_cols = []
    pivot_row = 0
    for col in range(n):
        found = -1
        for row in range(pivot_row, n):
            if matrix[row][col] == 1:
                found = row
                break
        if found == -1:
            continue
        matrix[pivot_row], matrix[found] = matrix[found], matrix[pivot_row]
        pivot_cols.append((pivot_row, col))
        for row in range(n):
            if row != pivot_row and matrix[row][col] == 1:
                matrix[row] = [matrix[row][k] ^ matrix[pivot_row][k] for k in range(n + 1)]
        pivot_row += 1

    solution = [0] * n
    for pr, pc in pivot_cols:
        solution[pc] = matrix[pr][n]

    return bits_to_bytes(solution)

with open('output.txt') as f:
    data = json.load(f)

zero_ct = bytes.fromhex(data['zero']['ct'])
flag_ct = bytes.fromhex(data['flag_ct'])

# Build columns of the linear map: col_i = bits(encrypt(e_i) XOR encrypt(0))
cols = []
for pair in data['basis_pairs']:
    ei_ct = bytes.fromhex(pair['ct'])
    col = bytes_to_bits(xor_bytes(ei_ct, zero_ct))
    cols.append(col)

# Decrypt each 16-byte block independently (ECB mode)
BLOCK = 16
plaintext = b''
for i in range(0, len(flag_ct), BLOCK):
    block_ct = flag_ct[i:i+BLOCK]
    block_pt = solve_block(block_ct, zero_ct, cols)
    print(f"Block {i//BLOCK}: {block_pt.hex()} -> {block_pt}")
    plaintext += block_pt

# Remove PKCS7 padding
pad_len = plaintext[-1]
if 1 <= pad_len <= 16 and plaintext[-pad_len:] == bytes([pad_len]*pad_len):
    plaintext = plaintext[:-pad_len]

print()
print("Full plaintext:", plaintext)
try:
    print("Flag:", plaintext.decode())
except:
    print("(not valid utf-8)")