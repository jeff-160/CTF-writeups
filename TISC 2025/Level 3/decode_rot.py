def decrypt(plain, key):
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{}_"
    shift = key
    cipher = ""
    for char in plain:
            index = charset.index(char)
            cipher += (charset[(index - shift) % len(charset)])
            shift = (shift + key) % len(charset)

    return cipher

enc = "aWnegWRi18LwQXnXgxqEF}blhs6G2cVU_hOz3BEM2{fjTb4BI4VEovv8kISWcks4"

key = 1

while True:
    flag = decrypt(enc, key)
    print("Key:", key, "|", "Flag:", flag)

    if "tisc" in flag.lower():
        break

    key += 1