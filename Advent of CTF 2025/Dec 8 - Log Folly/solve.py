import re

def solve(p, g, leaks):
    n = len(leaks)
    
    phi = p - 1  
    pow256n_mod = pow(256, n, phi)
    mult_base = (pow256n_mod - 1) % phi  

    bytes_out = []
    for i in range(n):
        h = leaks[i]
        h_next = leaks[(i + 1) % n]  
        rhs = pow(h, 256, p)  
        found = None
        
        for b in range(256):
            exp = (mult_base * b) % phi
            term = pow(g, exp, p)  
            if (h_next * term) % p == rhs:
                found = b
                break

        bytes_out.append(found)
    
    flag = bytes(bytes_out)
    return flag.decode()

with open("out.txt", "r") as f:
    contents = f.read().strip().split('\n')

p = int(re.findall(r'p:(.+)', contents[0])[0].strip())
leaks = [int(re.findall(r'leak:(.+)', line)[0].strip()) for line in contents[1:]]
g = 2

flag = solve(p, g, leaks)
print("Flag:", flag)