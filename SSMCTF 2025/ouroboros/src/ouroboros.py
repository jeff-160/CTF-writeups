exec('''import re, uuid, os, glob;pattern = '\\s*exec.*\\(*\\)|while.*|^(\\s{4})';filename = f'/tmp/instance_{uuid.uuid4()}.py';f = open(filename, 'w');f.write(re.sub(pattern, '', open(__file__).read(), flags=re.MULTILINE));f.close();rnd = 0;nono=r'!@$flag%^&*()+\~`,_./[]{}<>/?|=';script=open(filename).read();limit=1;run=True;debug_log=[]''')
while run:
    try:
        exec("char, index = input('feed me > ').split(' ')")
        exec("debug_log.append([char, index])")
        index = int(index)
        script = open(filename).read()
        exec("assert len(char) <= limit, 'too much food!'")
        exec("assert char not in nono, f'the ouroboros spits {char} out!'")
        exec("assert 1 < index < len(script), 'too far!'")
        exec("assert rnd < 1, 'time is up!'")
        script = script[:index-1] + char + script[index:]
        newfile = open(filename, 'w')
        newfile.write(script)
        newfile.close()
        exec("print(script)")
        exec(script)
        rnd = rnd+1
    except Exception as e:
        print(script, '\n-------\n', f'error: {e}')
        if 'instance' in filename: 
            os.remove(filename)
        for n in debug_log:
            print(n)
        run = False