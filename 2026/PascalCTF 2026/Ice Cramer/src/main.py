import os
from random import randint

def generate_variable():
    flag = os.getenv("FLAG", "pascalCTF{REDACTED}") # The default value is a placeholder NOT the actual flag
    flag = flag.replace("pascalCTF{", "").replace("}", "")
    x = [ord(i) for i in flag]
    return x

def generate_system(values):
    for _ in values:
        eq = []
        sol = 0
        for i in range(len(values)):
            k = randint(-100, 100)
            eq.append(f"{k}*x_{i}")
            sol += k * values[i]

        streq = " + ".join(eq) + " = " + str(sol)
        print(streq)


def main():
    x = generate_variable()
    generate_system(x)
    print("\nSolve the system of equations to find the flag!")

if __name__ == "__main__":
    main()