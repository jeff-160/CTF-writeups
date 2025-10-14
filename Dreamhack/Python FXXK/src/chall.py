import unicodedata

def checker(user_input):
    allowed_letter="aelprv()[]+" # Yes, you can code with only these!!
    test = unicodedata.normalize('NFKC', user_input) # No Hack~ ^_^
    if user_input!=test:
        return False
    for i in range(0,len(test),1):
        x=test[i]
        if x not in allowed_letter: # Whitelist!
            return False
    return True
        
print("Welcome to PythonFuck challenge!")
print("Show me your code written in PythonFuck!")
x=input('> ')

result=checker(x)

if result==True:
    print("Let's execute this!",flush=True)
    try:
        exec(x)
    except:
        pass
else:
    print("Not a PythonFuck code!")