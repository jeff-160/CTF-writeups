import requests
import itertools
import os

url = "http://fickle-tempest.picoctf.net:63750"

res = requests.get(f'{url}/bytes')
bytes_data = [int(b) for b in res.text.strip().split(" ")]

# get all possible key combinations
def get_keys():
    LEN = 16
    png_header = [137, 80, 78, 71, 13, 10, 26, 10]
    ihdr_start = [0, 0, 0, 13, 73, 72, 68, 82]  
    
    expected_first_16 = png_header + ihdr_start[:8]
    
    shifts = []
    
    for i in range(LEN):
        expected_byte = expected_first_16[i]
        valid_shifts = []
        
        for shift in range(10):  
            src_index = (((0 + shift) * LEN) % len(bytes_data)) + i
            
            if src_index < len(bytes_data) and bytes_data[src_index] == expected_byte:
                valid_shifts.append(shift)
        
        shifts.append(valid_shifts)
    
    return [''.join(str(x) for x in key_tuple) for key_tuple in itertools.product(*shifts)]

# assemble and save png
DIR = "save"

def save_png(bytes_data, key, filename):
    if not os.path.isdir(DIR):
        os.mkdir(DIR)

    LEN = 16
    result = [0] * len(bytes_data)
    
    for i in range(LEN):
        shifter = int(key[i])
        
        for j in range(len(bytes_data) // LEN):
            src_index = (((j + shifter) * LEN) % len(bytes_data)) + i
            dst_index = (j * LEN) + i
            
            if dst_index < len(result) and src_index < len(bytes_data):
                result[dst_index] = bytes_data[src_index]
    
    while result and result[-1] == 0:
        result.pop()

    with open(filename, 'wb') as f:
        f.write(bytes(result))
    
    print(f"Saved as {filename}")

# bruteforce
keys = get_keys()
    
for idx, key in enumerate(keys, start=1):
    save_png(bytes_data, key, f'{DIR}/out-{idx}.png')