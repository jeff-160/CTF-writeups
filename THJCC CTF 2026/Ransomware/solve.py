import hashlib
from Crypto.Cipher import AES

with open("src/desk/flag.txt.lock", "rb") as f:
    data = f.read()

unix_time = int.from_bytes(data[:8], "little")
iv = data[8:24]
ciphertext = data[24:]

key = hashlib.md5(str(unix_time).encode()).digest()

cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(ciphertext)

pad_len = plaintext[-1]
plaintext = plaintext[:-pad_len]

print("Flag:", plaintext.decode())