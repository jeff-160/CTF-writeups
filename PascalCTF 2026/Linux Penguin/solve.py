from pwn import *
import re

HOST = "penguin.ctf.pascalctf.it"
PORT = 5003

words = [
    "biocompatibility", "biodegradability", "characterization", "contraindication",
    "counterbalancing", "counterintuitive", "decentralization", "disproportionate",
    "electrochemistry", "electromagnetism", "environmentalist", "internationality",
    "internationalism", "institutionalize", "microlithography", "microphotography",
    "misappropriation", "mischaracterized", "miscommunication", "misunderstanding",
    "photolithography", "phonocardiograph", "psychophysiology", "rationalizations",
    "representational", "responsibilities", "transcontinental", "unconstitutional"
]

io = remote(HOST, PORT)

io.recvuntil(b"Welcome to the Penguin's Challenge!")

cipher_map = {}

for i in range(0, len(words), 4):
    io.recvuntil(b"Give me 4 words to encrypt")

    batch = words[i:i+4]

    for j, w in enumerate(batch):
        io.recvuntil(f"Word {j+1}: ".encode())
        io.sendline(w.encode())

    io.recvuntil(b"Encrypted words: ")
    enc = io.recvline().strip().decode().split()

    for w, c in zip(batch, enc):
        cipher_map[c] = w

io.recvuntil(b"Ciphertext: ")
challenge_ct = io.recvline().strip().decode().split()

recovered = [cipher_map[c] for c in challenge_ct]
log.success(f"Recovered words: {recovered}")

for i, w in enumerate(recovered):
    io.recvuntil(f"Guess the word {i+1}: ".encode())
    io.sendline(w.encode())

resp = io.recvall().decode()
io.close()

flag = re.findall(r'(pascalCTF{.+})', resp)[0]
print("Flag:", flag)