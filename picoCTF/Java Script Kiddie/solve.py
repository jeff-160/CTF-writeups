import requests
import itertools
import os

url = "http://fickle-tempest.picoctf.net:59080"

res = requests.get(f"{url}/bytes")
bytes_data = [int(b) for b in res.text.strip().split(" ")]

# get all possible key combinations
def get_keys(bytes_data):
    png_header = [137, 80, 78, 71, 13, 10, 26, 10]
    ihdr_start = [0, 0, 0, 13, 73, 72, 68, 82]  
    
    LEN = 16
    rows = len(bytes_data) // LEN
    
    possible_shifts = [[] for _ in range(LEN)]
    
    for col in range(8):
        for shift in range(10):
            original_row = shift % rows
            idx = (original_row * LEN) + col
            if idx < len(bytes_data) and bytes_data[idx] == png_header[col]:
                possible_shifts[col].append(shift)
    
    for col in range(8):
        if len(possible_shifts[col]) > 1:
            new_possible = []
            for shift in possible_shifts[col]:            
                original_row = (1 + shift) % rows
                idx = (original_row * LEN) + col
                if idx < len(bytes_data) and bytes_data[idx] == ihdr_start[col]:
                    new_possible.append(shift)
            if new_possible:
                possible_shifts[col] = new_possible
    
    for col in range(8, 16):
        
        target_byte = ihdr_start[col - 8]
        for shift in range(10):
            original_row = shift % rows
            idx = (original_row * LEN) + col
            if idx < len(bytes_data) and bytes_data[idx] == target_byte:
                possible_shifts[col].append(shift)

    return [''.join(str(digit) for digit in combination) for combination in itertools.product(*possible_shifts)]

# decrypt and save png
DIR = "save"

def save_png(bytes_data, key, filename):
    if not os.path.isdir(DIR):
        os.mkdir(DIR)

    LEN = 16
    result = [0] * len(bytes_data)
    
    for i in range(LEN):
        shifter = int(key[i])
        for j in range(len(bytes_data) // LEN):
            result[(j * LEN) + i] = bytes_data[(((j + shifter) * LEN) % len(bytes_data)) + i]
    
    while result and result[-1] == 0:
        result = result[:-1]
    
    with open(filename, 'wb') as f:
        f.write(bytes(result))

    print(f"Saved as {filename}")

# bruteforce all combinations
keys = get_keys(bytes_data)

for idx, key in enumerate(keys, start=1):
    save_png(bytes_data, key, f'{DIR}/out-{idx}.png')