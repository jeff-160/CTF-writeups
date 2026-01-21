def func1(n):
    count = 0
    while n > 0:
        if n & 1:
            count = func2(count)
        n = n >> 1
    return count

def func2(x):
    return x + 3

result = func1(4101707659)
flag = format(result & 0xFFFFFFFF, '08x')

print("Flag: picoCTF{%s}" % flag)