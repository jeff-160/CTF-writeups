from pwn import *
import re

io = remote('auratester.ctf.pascalctf.it', 7001)

# name
io.sendlineafter(b'name.', b'hackerman')

# farm aura
io.sendlineafter(b'little Beta?', b'1')

for ans in ['yes', 'no', 'yes', 'no']:
    io.sendlineafter(b">", ans.encode())

# aura test
def decrypt(cipher, steps):
    result = ""
    i = j = 0 

    while j < len(cipher):
        if cipher[j] == " ":
            result += " "
            j += 1
            i += 1
            continue

        if i % steps == 0:
            num = ""
            while j < len(cipher) and cipher[j].isdigit():
                num += cipher[j]
                j += 1

            if num == "":
                return None

            result += chr(int(num))
            i += 1
        else:
            result += cipher[j]
            j += 1
            i += 1

    return result

def solve(cipher):
    for i in range(2, 6):
        secret = decrypt(cipher, i)
        print(secret)

        if secret:
            return secret
        
        i += 1

io.sendlineafter(b'little Beta?', b'3')

io.recvuntil(b'phrase:')

enc = io.recvuntil(b'Type', drop=True).decode().strip()

io.sendlineafter(b'>', solve(enc).encode())

resp = io.recvall().decode()
io.close()

flag = re.findall(r'(pascalCTF{.+})', resp)[0]
print("Flag:", flag)