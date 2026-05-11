

SEED = 0xBE35
EMBED_DIM = 256
CHARSET = "".join(chr(i) for i in range(32, 127))
CHAR_TO_IDX = {c: i for i, c in enumerate(CHARSET)}
MAX_LEN = 64


class EmbeddingModel:
    """
    Character-level embedding with positional entanglement.

    For each character at position i:
        v_i = (char_matrix[c] * pos_scale[i]) + pos_bias[i]

    Output = mean(v_0, ..., v_{n-1}) @ projection

    The elementwise multiply with pos_scale makes each character's
    contribution depend on its position — the model is sensitive
    to character ORDER, not just content.
    """
    def __init__(self, seed=SEED):
        rng = np.random.RandomState(seed)
        self.char_matrix = rng.randn(len(CHARSET), EMBED_DIM) * 0.3
        self.pos_scale   = rng.randn(MAX_LEN, EMBED_DIM) * 0.5 + 1.0
        self.pos_bias    = rng.randn(MAX_LEN, EMBED_DIM) * 0.1
        # Orthogonal projection preserves distances and conditioning
        P = rng.randn(EMBED_DIM, EMBED_DIM)
        self.projection, _ = np.linalg.qr(P)

    def _char_contribution(self, char_idx, pos):
        return self.char_matrix[char_idx] * self.pos_scale[pos] + self.pos_bias[pos]

    def embed(self, text: str) -> np.ndarray:
        text = text[:MAX_LEN]
        if len(text) == 0:
            return np.zeros(EMBED_DIM)
        vecs = []
        for i, c in enumerate(text):
            if c not in CHAR_TO_IDX:
                raise ValueError(f"Character {repr(c)} not in charset")
            vecs.append(self._char_contribution(CHAR_TO_IDX[c], i))
        return np.mean(vecs, axis=0) @ self.projection

    def embed_positional_matrix(self, pos, n):
        """
        Returns (|CHARSET|, EMBED_DIM) matrix where row c =
        contribution of charset[c] at position pos in a length-n string.
        """
        contrib = (self.char_matrix * self.pos_scale[pos]) + self.pos_bias[pos]
        return (contrib / n) @ self.projection


def generate_rotation(dim, seed):
    """Generate a random orthogonal (rotation) matrix."""
    rng = np.random.RandomState(seed)
    Q, _ = np.linalg.qr(rng.randn(dim, dim))
    if np.linalg.det(Q) < 0:
        Q[:, 0] *= -1
    return Q


def generate_challenge(output_dir="inversions/"):
    os.makedirs(output_dir, exist_ok=True)
    model = EmbeddingModel()

    # Secret rotation + noise
    rotation = generate_rotation(EMBED_DIM, ROTATION_SEED)
    noise_scale = 0.008
    noise_rng = np.random.RandomState(NOISE_SEED)

    # Protected flag embedding
    flag_embedding = model.embed(FLAG) @ rotation + noise_rng.randn(EMBED_DIM) * noise_scale

    # Generate dataset of known triples
    print("  Generating dataset of known triples...")
    probe_rng = np.random.RandomState(PROBE_SEED)
    dataset = []

    for i in range(350):
        length = probe_rng.randint(5, 40)
        text = "".join(CHARSET[probe_rng.randint(len(CHARSET))] for _ in range(length))

        clean_emb = model.embed(text)
        protected_emb = clean_emb @ rotation + noise_rng.randn(EMBED_DIM) * noise_scale

        dataset.append({
            "string": text,
            "clean_embedding": clean_emb.tolist(),
            "protected_embedding": protected_emb.tolist()
        })
        
    # Saving flag embedding
    challenge_data = {
        "flag_embedding": flag_embedding.tolist(),
        "flag_length": len(FLAG),
        "flag_format": "Cyberthon{[a-z0-9_]+}",
        "flag_sha256": hashlib.sha256(FLAG.encode()).hexdigest(),
        "noise_scale": noise_scale,
    }
    
    with open(os.path.join(output_dir, "challenge.json"), "w") as f:
        json.dump(challenge_data, f, indent=2)

    with open(os.path.join(output_dir, "dataset.json"), "w") as f:
        json.dump(dataset, f)
        
    print("Finished Generating Challenge!")
    print(f"{FLAG = }")
    print(f"{len(FLAG) = }")
    print(f"{hashlib.sha256(FLAG.encode()).hexdigest() = }")

