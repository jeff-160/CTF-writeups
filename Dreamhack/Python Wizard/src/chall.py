import unicodedata
import _frozen_importlib

def filter_spell(user_input):
    banned_character="\'\"\\!@#$%^&|`~+-*/=:;<>,?{}[]"
    banned_word=['eval', 'exec', 'import', 'open', 'os', 'sys', 'read', 'system', 'write', 'sh', 'break', 'mro', 'cat', 'flag']
    test = unicodedata.normalize('NFKC', user_input)
    if user_input!=test:
        return False
    for i in range(0,len(banned_word),1):
        x=banned_word[i]
        if x in test:
            print(x)
            return False
    for i in range(0,len(banned_character),1):
        x=banned_character[i]
        if x in test:
            print
            return False
    return True

print("My magic filter is notoriously stubborn. Prove that you are a true wizard.")
spell=input('Cast your spell > ')
result=filter_spell(spell)

if result==True:
    try:
        loc={}
        bytecode=compile(spell,'','exec')
        try:
            print('Alright then, show your power!!',flush=True)
            exec(bytecode,{'__builtins__':None, '__loader__':_frozen_importlib.BuiltinImporter},loc)
        except:
            print('Your spell had technical issue...')
        finally:
            print('I am still here! Try again.')
    except:
        print('Your spell was invalid!')
else:
    print('Alas, your spell was blocked! My filter remains unbroken.')

