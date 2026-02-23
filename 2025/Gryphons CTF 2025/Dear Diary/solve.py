def remove_spacing(text):
    return text.replace(" ", "")

def reverse_mod_transform(text, mod_values):
    result = list(text)
    
    for iteration in reversed(range(5)):
        mod_val = mod_values[iteration]
        transformed = []
        for i, c in enumerate(result):
            if c.isalpha():
                offset = (ord(c) - ord('A') - mod_val - i) % 26
                transformed.append(chr(ord('A') + offset))
            else:
                transformed.append(c)
        result = transformed
    return "".join(result)

def reverse_rail_fence(ciphertext, num_rails):
    if num_rails <= 1:
        return ciphertext
    
    
    rail_lengths = [0] * num_rails
    n = len(ciphertext)
    
    
    rail = 0
    direction_down = True
    for i in range(n):
        rail_lengths[rail] += 1
        if rail == 0:
            direction_down = True
        elif rail == num_rails - 1:
            direction_down = False
        rail += 1 if direction_down else -1
    
    
    rails = []
    idx = 0
    for length in rail_lengths:
        rails.append(list(ciphertext[idx:idx+length]))
        idx += length
    
    
    result = []
    rail = 0
    direction_down = True
    for i in range(n):
        result.append(rails[rail].pop(0))
        if rail == 0:
            direction_down = True
        elif rail == num_rails - 1:
            direction_down = False
        rail += 1 if direction_down else -1
    return "".join(result)

def decrypt(ciphertext):
    mod_values = [10, 17, 24, 31, 38]  
    text_no_spaces = remove_spacing(ciphertext)
    mod_reversed = reverse_mod_transform(text_no_spaces, mod_values)
    plaintext = reverse_rail_fence(mod_reversed, 3)  
    return plaintext


ciphertext = "W2CY7 RZ5RA DBE2B RQK6"
flag = decrypt(ciphertext)
print(flag)