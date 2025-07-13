def generate_flag(index):
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]|;:,.<>?~` "
    base = len(charset)
    max_len = 57

    tV = [base ** i for i in range(1, max_len + 1)]

    if index < 0:
        raise ValueError("Index must be non-negative")

    t = 0
    for r, a in enumerate(tV):
        if index < t + a:
            length = r + 1
            break
        t += a
    else:
        raise ValueError("Index out of range")

    offset = index - t
    flag_chars = []
    for _ in range(length):
        flag_chars.append(charset[offset % base])
        offset //= base

    return "LNC25{" + ''.join(reversed(flag_chars)) + "}"

print(generate_flag(10941413769315357217397039591847663286726867611759942474129155219182958797137888157553105496655320663))