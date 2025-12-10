import z3
import struct

def predict(sequence):
    sequence = sequence[::-1]

    solver = z3.Solver()

    se_state0, se_state1 = z3.BitVecs("se_state0 se_state1", 64)

    for i in range(len(sequence)):
        se_s1 = se_state0
        se_s0 = se_state1
        se_state0 = se_s0
        se_s1 ^= se_s1 << 23
        se_s1 ^= z3.LShR(se_s1, 17)
        se_s1 ^= se_s0
        se_s1 ^= z3.LShR(se_s0, 26)
        se_state1 = se_s1

        float_64 = struct.pack("d", sequence[i] + 1)
        u_long_long_64 = struct.unpack("<Q", float_64)[0]

        mantissa = u_long_long_64 & ((1 << 52) - 1)

        solver.add(int(mantissa) == z3.LShR(se_state0, 12))

    if solver.check() == z3.sat:
        model = solver.model()

        states = {}
        for state in model.decls():
            states[state.__str__()] = model[state]

        state0 = states["se_state0"].as_long()

        u_long_long_64 = (state0 >> 12) | 0x3FF0000000000000
        float_64 = struct.pack("<Q", u_long_long_64)
        next_sequence = struct.unpack("d", float_64)[0]
        next_sequence -= 1

        return next_sequence
    else:
        return None
    
def solve(seq, n):
    results = []

    for _ in range(n):
        next_n = predict(seq)
        results.append(next_n)

        seq = seq[1:] + [next_n]

    return results