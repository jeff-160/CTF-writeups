from flask import Flask, render_template, request
import unicodedata

app=Flask(__name__)

def filter_code(user_input):
    banned_character="\'\"\\!@#$%^&*;:?_=<>~`"
    banned_word=['eval', 'exec', 'import', 'open', 'os', 'sys', 'read', 'system', 'write', 'sh', 'break', 'mro', 'cat', 'flag', 'ascii', 'breakpoint', 'globals', 'init']
    test = unicodedata.normalize('NFKC', user_input)
    if user_input!=test:
        return False
    for i in range(0,len(banned_word),1):
        x=banned_word[i]
        if x in test:
            return False
    for i in range(0,len(banned_character),1):
        x=banned_character[i]
        if x in test:
            return False
    return True

@app.route("/")
def main():
    return render_template('main.html')

@app.route("/submit",methods=['POST'])
def run():
    code=request.form.get('code')
    result=filter_code(code)
    if result==True:
        try:
            exec(code)
        except:
            pass
        finally:
            return render_template('main.html',error="Hacked!")
    else:
        return render_template('main.html',error="No Hack~ ^_^")

if __name__=='__main__':
    app.run(debug=False,host='0.0.0.0',port=5000)