f = open('flag.txt').read()

for _ in range(2):
    command = input(">>> ")
    if len(command) > 5:
        print("Command too long!")
        continue
    
    try:
        exec(command)
    except Exception:
        print("Something went wrong!")

print("You out of prompts :(")