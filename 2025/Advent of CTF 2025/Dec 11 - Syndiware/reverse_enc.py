import os

DIST = "syndicate_locker"
OUT = "decrypted"

def xor_decrypt(data, key):
    output = bytearray()
    key_len = len(key)
    for i, byte in enumerate(data):
        output.append(byte ^ key[i % key_len])
    return bytes(output)

def parse_memory_dump(dump_file):
    with open(dump_file, 'rb') as f:
        dump_data = f.read()
    
    marker = b'\xAA\xBB\xCC\xDD'
    results = []
    
    i = 0
    while i < len(dump_data) - 4:
        if dump_data[i : i + 4] == marker:
            
            key_start = i - 32
            if key_start >= 0:
                key = dump_data[key_start:i]
                
                filename_start = key_start - 60
                if filename_start >= 0:
                    filename_bytes = dump_data[filename_start:key_start]
                    
                    filename = filename_bytes.rstrip(b'\x00').decode('utf-8', errors='ignore')
                    
                    if filename and '.' in filename and len(filename) > 1:
                        results.append((filename, key))
                        print(f"Found: {filename}")
        i += 1
    
    return results

def decrypt_files(file_key_pairs):
    for original_filename, key in file_key_pairs:
        encrypted_file = f'{DIST}/encrypted_files/{original_filename}.enc'
        
        with open(encrypted_file, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = xor_decrypt(encrypted_data, key)

        if not os.path.isdir(OUT):
            os.makedirs(OUT)
        
        with open(f'{OUT}/{original_filename}', 'wb') as f:
            f.write(decrypted_data)
        
        print(f"Decrypted: {original_filename}")

file_key_pairs = parse_memory_dump(f'{DIST}/ransomware.dmp')    
decrypt_files(file_key_pairs)