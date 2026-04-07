from pwn import *

io = remote("chall1.lagncra.sh", 18376)
context.log_level = 'debug'

def get_word(sentence):
    words = sentence.split(" ")

    for word in words:
        last_char = None

        for char in word:
            if char == last_char:
                return word

            last_char = char

io.recvuntil(b'ck!')

io.recvuntil(b'Aufgabe')

for _ in range(250):
    io.recvuntil(b'Aufgabe')
    io.recvline()

    sentence = io.recvuntil(':', drop=True).decode().strip()
    log.info(f'Sentence: {sentence}')

    answer = get_word(sentence)
    log.info(f'Answer: {answer}')

    io.sendline(answer.encode())
    io.recvline()

io.interactive()