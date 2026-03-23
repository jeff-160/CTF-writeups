code = input("code> ")[:100 + 20 + 3]

if not code.isascii():
    print("bye")
    exit(1)

# i hate math
if any(c in code for c in '+-*/='):
    print("bye")
    exit(1)

min_len = 1337
for m in __import__("re").finditer(r"\w+", code):
    if len(m[0]) >= min_len:
        print("bye")
        exit(1)
    min_len = len(m[0])

eval(code, {"__builtins__": {}})
