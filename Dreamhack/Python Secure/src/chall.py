import unicodedata

def filter(user_input):
    banned_character="\\!@#$%^&|`~+-*/=;<>.?{}[]0123456789"
    banned_word=['eval', 'exec', 'import', 'open', 'os', 'sys', 'read', 'system', 'write', 'sh', 'break', 'mro', 'cat', 'flag','self','built','class','base','module','chr','init','h']
    test = unicodedata.normalize('NFKC', user_input)
    if user_input!=test:
        return False
    if(len(test)>60):
        print("Length exceeded")
        return False
    for i in range(0,len(banned_word),1):
        x=banned_word[i]
        if x in test:
            print("Blacklisted:", x)
            return False
    for i in range(0,len(banned_character),1):
        x=banned_character[i]
        if x in test:
            print("Blacklisted:", x)
            return False
    return True

print("Python 3.12.R [GCC 13.3.0] on linux")
print("Restricted Python environment, Developed by Rootsquare.")
while True:
    code=input('>>> ')
    try:
        result=filter(code)
        if result==True:
            try:
                exec(code)
            except:
                print('Error!')
        else:
            print('No Hack~ ^_^')
    except:
        print('No Hack~ ^_^')