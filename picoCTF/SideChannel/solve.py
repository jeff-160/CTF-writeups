from pwn import *
import time
from statistics import median

pin = ""

while len(pin) < 8:
    times = {}
    
    for i in range(0, 10):
        samples = []

        for _ in range(10):
            p = process("./pin_checker")
            guess = f'{pin}{i}'.ljust(8, '0')

            p.info(f"Trying: {guess}")
            
            start = time.perf_counter()
            p.sendlineafter(b':', guess.encode())
            p.recvall()
            end = time.perf_counter()

            samples.append(end - start)

            p.close()
    
        times[i] = median(samples)
    
    pin += str(max(times, key=lambda x: times[x]))

print("Pin:", pin)

r = remote("saturn.picoctf.net", 56543)
r.sendlineafter(b":", pin.encode())

resp = r.recvall().decode()
r.close()

flag = re.findall(r'(picoCTF{.+})', resp)[0]
print("Flag:", flag)