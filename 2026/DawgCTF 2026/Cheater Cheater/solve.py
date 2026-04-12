from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

n = 6942069
val = (n*10 + 1)**4
s = str(val)

def hexStringToByteArray(s):
    return bytes(int(s[i:i+2], 16) for i in range(0, len(s), 2))

key = hexStringToByteArray(s)[0:16]
iv  = hexStringToByteArray(s[::-1])[0:16]

ct = b64decode("6Ach6HiD0JmCc1L+RwxDRzhW3sC1kS6XydgSuWVFpxVXRU8EjfuMxIMoIzMwK/ii")

cipher = AES.new(key, AES.MODE_CBC, iv)
pt = unpad(cipher.decrypt(ct), 16)

print("Flag:", pt.decode())