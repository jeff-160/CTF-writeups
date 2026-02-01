from Crypto.Cipher import AES
import random
import os

key = os.urandom(16)
cipher = AES.new(key, AES.MODE_ECB)

words = [
    "biocompatibility", "biodegradability", "characterization", "contraindication",
    "counterbalancing", "counterintuitive", "decentralization", "disproportionate",
    "electrochemistry", "electromagnetism", "environmentalist", "internationality",
    "internationalism", "institutionalize", "microlithography", "microphotography",
    "misappropriation", "mischaracterized", "miscommunication", "misunderstanding",
    "photolithography", "phonocardiograph", "psychophysiology", "rationalizations",
    "representational", "responsibilities", "transcontinental", "unconstitutional"
]

def print_flag():
    flag = os.getenv("FLAG", "pascalCTF{REDACTED}")
    print(flag)

def encrypt_words(wordst: list[str]) -> list[str]:
    encrypted_words = []
    for word in wordst:
        padded_word = word.ljust(16)
        encrypted = cipher.encrypt(padded_word.encode()).hex()
        encrypted_words.append(encrypted)
    return encrypted_words

def wallpaper():
    print("""
                 .88888888:.
                88888888.88888.
              .8888888888888888.
              888888888888888888
              88' _`88'_  `88888
              88 88 88 88  88888
              88_88_::_88_:88888
              88:::,::,:::::8888
              88`:::::::::'`8888
             .88  `::::'    8:88.
            8888            `8:888.
          .8888'             `888888.
         .8888:..  .::.  ...:'8888888:.
        .8888.'     :'     `'::`88:88888
       .8888        '         `.888:8888.
      888:8         .           888:88888
    .888:88        .:           888:88888:
    8888888.       ::           88:888888
    `.::.888.      ::          .88888888
   .::::::.888.    ::         :::`8888'.:.
  ::::::::::.888   '         .::::::::::::
  ::::::::::::.8    '      .:8::::::::::::.
 .::::::::::::::.        .:888:::::::::::::
 :::::::::::::::88:.__..:88888:::::::::::'
  `'.:::::::::::88888888888.88:::::::::'
        `':::_:' -- '' -'-' `':_::::'`  
    """)

    print("Welcome to the Penguin's Challenge!")


def main():
    wallpaper()
    
    selected_words = random.choices(words, k=5)
    ciphertext = ' '.join(encrypt_words(selected_words))
    
    for i in range(7):
        print("Give me 4 words to encrypt or don't write anything to quit (max 16 chars):")
    
        user_words = [
            input(f"Word {j+1}: ").strip() for j in range(4)
        ]

        if any(len(word) > 16 for word in user_words):
            print("Invalid input. Please enter words with a maximum of 16 characters.")
            continue

        if any(word == '' for word in user_words):
            print("Exiting the challenge.")
            break

        encrypted_words = encrypt_words(user_words)
        print(f"Encrypted words: {' '.join(encrypted_words)}")

    print("Can you now guess what are these encrypted words?")
    print(f"Ciphertext: {ciphertext}")

    for i in range(5):
        guess = input(f"Guess the word {i+1}: ")
        if guess not in selected_words:
            print("Wrong guess. Try again.")
            return
        print(f"Correct guess: {guess}")
        selected_words.remove(guess)

    print_flag()

if __name__ == "__main__":
    main()