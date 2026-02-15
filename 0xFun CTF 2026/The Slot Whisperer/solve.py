from pwn import *

M = 2147483647
A = 48271
C = 12345

HOST = "chall.0xfun.org"
PORT = 32962

def next_state(state):
    return (A * state + C) % M

def recover_state(observed):
    candidates = []

    for s in range(observed[0], M, 100):
        state = s
        valid = True

        for spin in observed[1:]:
            state = next_state(state)
            if state % 100 != spin:
                valid = False
                break

        if valid:
            candidates.append(s)

    return candidates

def main():
    r = remote(HOST, PORT)

    observed = []

    while True:
        data = r.recv(timeout=2).decode()
        print(data, end="")

        for line in data.split("\n"):
            line = line.strip()
            if line.isdigit():
                observed.append(int(line))

        if "Predict the next 5 spins" in data:
            break

    print("\n[+] Observed spins:", observed)

    candidates = recover_state(observed[:6])
    print(f"[+] Found {len(candidates)} candidates")

    valid_states = []

    for s in candidates:
        state = s
        valid = True

        for spin in observed[1:]:
            state = next_state(state)
            if state % 100 != spin:
                valid = False
                break

        if valid:
            valid_states.append(state)

    print(f"[+] Remaining valid states: {len(valid_states)}")

    if not valid_states:
        print("[-] Failed to determine state")
        return

    state = valid_states[0]

    # Generate next 5 spins
    predictions = []
    for _ in range(5):
        state = next_state(state)
        predictions.append(str(state % 100))

    payload = " ".join(predictions)
    print(f"[+] Sending: {payload}")

    r.sendline(payload.encode())
    r.interactive()

if __name__ == "__main__":
    main()
