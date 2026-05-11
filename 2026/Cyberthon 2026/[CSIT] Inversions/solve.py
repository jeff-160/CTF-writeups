import json
import math
import numpy as np
import string

# ── Load challenge data ────────────────────────────────────────────────────────
challenge  = json.load(open("challenge.json"))
dataset    = json.load(open("dataset.json"))

flag_emb   = np.array(challenge["flag_embedding"])
flag_len   = challenge["flag_length"]          # FIX 1: use actual length (29), not MAX_LEN (64)
target_sha = challenge["flag_sha256"]

# ── Model constants ────────────────────────────────────────────────────────────
SEED    = 0xBE35
DIM     = 256
MAX_LEN = 64

# FIX 2: CHARSET must be the full range(32,127) used during training.
#         Using only ascii_lowercase+digits+"_" de-syncs the RNG so every
#         matrix (char_matrix, pos_scale, pos_bias, projection) is wrong.
FULL_CHARSET = "".join(chr(i) for i in range(32, 127))
full_c2i     = {c: i for i, c in enumerate(FULL_CHARSET)}

# Characters allowed inside the flag body  Cyberthon{<here>}
INNER = list(string.ascii_lowercase + string.digits + "_")

# ── Rebuild model (must match generation seed exactly) ────────────────────────
rng          = np.random.RandomState(SEED)
char_matrix  = rng.randn(len(FULL_CHARSET), DIM) * 0.3
pos_scale    = rng.randn(MAX_LEN, DIM) * 0.5 + 1.0
pos_bias     = rng.randn(MAX_LEN, DIM) * 0.1    # FIX 3: pos_bias was never drawn,
                                                  #         corrupting every matrix after it
P            = rng.randn(DIM, DIM)
proj, _      = np.linalg.qr(P)

def embed(text: str) -> np.ndarray:
    vecs = [char_matrix[full_c2i[c]] * pos_scale[i] + pos_bias[i]
            for i, c in enumerate(text)]
    return np.mean(vecs, axis=0) @ proj

# ── Recover the secret rotation matrix R from the dataset ─────────────────────
# Each pair satisfies:  protected = clean @ R + noise
# Stacking 350 pairs:   C @ R ≈ P  →  solve with lstsq
C_mat = np.array([d["clean_embedding"]     for d in dataset])
P_mat = np.array([d["protected_embedding"] for d in dataset])
R, _, _, _ = np.linalg.lstsq(C_mat, P_mat, rcond=None)

# ── Undo the rotation to recover the clean flag embedding ─────────────────────
clean_flag = flag_emb @ np.linalg.inv(R)

# ── Efficient delta-update helpers ────────────────────────────────────────────
PREFIX = "Cyberthon{"
SUFFIX = "}"
N      = flag_len
MID    = N - len(PREFIX) - len(SUFFIX)           # 18 inner characters

def char_contrib(c: str, j: int) -> np.ndarray:
    """Raw (pre-mean, pre-projection) contribution of inner char c at index j."""
    pos = len(PREFIX) + j
    return char_matrix[full_c2i[c]] * pos_scale[pos] + pos_bias[pos]

def full_sum(mid: list) -> np.ndarray:
    """Pre-mean, pre-projection sum over ALL characters in the candidate flag."""
    s = sum(char_matrix[full_c2i[c]] * pos_scale[i] + pos_bias[i]
            for i, c in enumerate(PREFIX))
    s += sum(char_contrib(c, j) for j, c in enumerate(mid))
    s += char_matrix[full_c2i[SUFFIX]] * pos_scale[N - 1] + pos_bias[N - 1]
    return s

def score_sum(s: np.ndarray) -> float:
    """Score a pre-projection sum vector against the target."""
    return float(np.linalg.norm((s / N) @ proj - clean_flag))

# ── Greedy initialisation (best char at each position independently) ──────────
mid = ["a"] * MID
s   = full_sum(mid)
for j in range(MID):
    best_c, best_sc = mid[j], score_sum(s)
    for c in INNER:
        new_s  = s - char_contrib(mid[j], j) + char_contrib(c, j)
        new_sc = score_sum(new_s)
        if new_sc < best_sc:
            best_sc, best_c = new_sc, c
    s      = s - char_contrib(mid[j], j) + char_contrib(best_c, j)
    mid[j] = best_c

best, best_s, best_score = mid.copy(), s.copy(), score_sum(s)
print(f"Greedy init : score={best_score:.5f}  {PREFIX}{''.join(best)}{SUFFIX}")

# ── Simulated annealing with swap + change moves ──────────────────────────────
# FIX 4: add *swap* moves so the optimizer can reorder characters without
#         changing the character set — critical because the correct flag is
#         an anagram of the greedy result.
global_best, global_s, global_score = best.copy(), best_s.copy(), best_score

np.random.seed(0)
for trial in range(20):
    if trial == 0:
        mid = global_best.copy()
    else:
        mid = global_best.copy()
        for _ in range(np.random.randint(2, 5)):        # random swap perturbation
            i, j = np.random.choice(MID, 2, replace=False)
            mid[i], mid[j] = mid[j], mid[i]
        for _ in range(np.random.randint(1, 3)):        # random char perturbation
            i = np.random.randint(MID)
            mid[i] = np.random.choice(INNER)

    s  = full_sum(mid)
    sc = score_sum(s)
    T  = sc * 0.25

    for _ in range(300_000):
        move = np.random.randint(3)

        if move == 0:                                   # change one character
            j      = np.random.randint(MID)
            old_c  = mid[j]
            new_c  = np.random.choice(INNER)
            new_s  = s - char_contrib(old_c, j) + char_contrib(new_c, j)
            new_sc = score_sum(new_s)
            if new_sc < sc or np.random.random() < math.exp((sc - new_sc) / max(T, 1e-9)):
                mid[j], s, sc = new_c, new_s, new_sc

        elif move == 1:                                 # swap two positions
            i, j   = np.random.choice(MID, 2, replace=False)
            ci, cj = mid[i], mid[j]
            new_s  = (s
                      - char_contrib(ci, i) - char_contrib(cj, j)
                      + char_contrib(cj, i) + char_contrib(ci, j))
            new_sc = score_sum(new_s)
            if new_sc < sc or np.random.random() < math.exp((sc - new_sc) / max(T, 1e-9)):
                mid[i], mid[j], s, sc = cj, ci, new_s, new_sc

        else:                                           # change + potential swap
            j      = np.random.randint(MID)
            old_c  = mid[j]
            new_c  = np.random.choice(INNER)
            new_s  = s - char_contrib(old_c, j) + char_contrib(new_c, j)
            new_sc = score_sum(new_s)
            if new_sc < sc or np.random.random() < math.exp((sc - new_sc) / max(T, 1e-9)):
                mid[j], s, sc = new_c, new_s, new_sc
            else:
                mid[j] = old_c

        if sc < global_score:
            global_best, global_s, global_score = mid.copy(), s.copy(), sc

        T *= 0.99999

    candidate = PREFIX + "".join(global_best) + SUFFIX
    sha_ok    = (__import__("hashlib").sha256(candidate.encode()).hexdigest() == target_sha)
    print(f"trial={trial:2d}  score={global_score:.6f}  {candidate}  sha_ok={sha_ok}")
    if sha_ok:
        break

# ── Result ─────────────────────────────────────────────────────────────────────
import hashlib
flag   = PREFIX + "".join(global_best) + SUFFIX
sha_ok = hashlib.sha256(flag.encode()).hexdigest() == target_sha

print(f"\nFLAG: {flag}")
print(f"SHA match: {sha_ok}")