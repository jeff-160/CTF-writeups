FLAG = open('flag.txt').read().strip()
BANNED_CHARS = "abcddefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'!@#$%^&*()_+-=[]{}|;':\",.<>?/~`"

def check_violations(input: str) -> bool:
    for char in input:
        if char in BANNED_CHARS:
            return True
    return False

print("Welcome to the variable gift shop. Everything here is free... if you can get it!")
var = input("Enter a variable name: ")

if check_violations(var):
    print("You have violated the rules of the shop. You will be punished.")
else:
    try:
        value = eval(var, globals(), locals())
        print(value)
    except NameError:
        print("Whoops, you got me, I haven't had that variable in stock for a while.")
    except Exception:
        print("What are you trying to do???")
