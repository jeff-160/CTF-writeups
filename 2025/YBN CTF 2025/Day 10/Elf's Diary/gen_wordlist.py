prefixes = ["G", "D"]

min_number = 1
max_number = 9999

min_cabin = 1
max_cabin = 17

passwords = []

for prefix in prefixes:
    for train_num in range(min_number, max_number + 1):
        train_number = f"{prefix}{train_num:0>4}"
        for cabin in range(min_cabin, max_cabin + 1):
            passwords.append(f"{train_number}_{cabin:02d}")

with open("wordlist.txt", "w") as f:
    f.write('\n'.join(passwords))

print("> Wrote wordlist")