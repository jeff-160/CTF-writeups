def func1(w):
    if w <= 100:
        return func3(w)
    else:
        return func2(w + 100)

def func2(w):
    if w > 499:
        return func5(w + 13)
    else:
        return func4(w - 86)

def func3(w):
    return func7(w)

def func4(w):
    return w

def func5(w):
    return func8(w)

def func6(w):
    var24 = 314
    var28 = 1932
    var20 = 0
    while var20 <= 899:
        w = (var28 * 800) % var24
        var20 += 1
    return w

def func7(w):
    if w <= 100:
        return 7
    else:
        return w

def func8(w):
    return w + 2

def main(arg):
    return func1(arg)

result = main(1854822502)
print("Flag: picoCTF{%s}" % hex(result)[2:])