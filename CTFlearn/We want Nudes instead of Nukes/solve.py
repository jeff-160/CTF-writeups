from binascii import unhexlify, hexlify

iv_hex = "391e95a15847cfd95ecee8f7fe7efd66"
cipher_hex = "8473dcb86bc12c6b6087619c00b6657e"

original = b"FIRE_NUKES_MELA!"
target   = b"SEND_NUDES_MELA!"

iv = unhexlify(iv_hex)
new_iv = bytes(iv[i] ^ original[i] ^ target[i] for i in range(len(iv)))

print("Flag: flag{%s,%s}" % (hexlify(new_iv).decode(), cipher_hex))