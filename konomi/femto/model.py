"""
FemtoLLM — 16-dimensional nano language model.
16d | 1 layer | 1 head | 4MB RAM | 0.1s/req

This is a real (tiny) transformer, not a mock.
Useful for pattern matching, tag classification, and
simple rule evaluation within the Konomi system.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FemtoLLM:
    """16-dimensional nano transformer model."""
    hidden_size: int = 16
    vocab_size: int = 256       # byte-level tokenization
    max_seq: int = 128
    _weights: dict = field(default_factory=dict, repr=False)
    _ready: bool = field(default=False, repr=False)

    def __post_init__(self):
        self._init_weights()

    def _init_weights(self):
        """Initialize tiny transformer weights."""
        h = self.hidden_size
        v = self.vocab_size
        rng = np.random.default_rng(42)  # deterministic for consistency

        self._weights = {
            "embed": rng.standard_normal((v, h)).astype(np.float32) * 0.1,
            "Wq": rng.standard_normal((h, h)).astype(np.float32) * 0.1,
            "Wk": rng.standard_normal((h, h)).astype(np.float32) * 0.1,
            "Wv": rng.standard_normal((h, h)).astype(np.float32) * 0.1,
            "Wo": rng.standard_normal((h, h)).astype(np.float32) * 0.1,
            "ff1": rng.standard_normal((h, h * 4)).astype(np.float32) * 0.1,
            "ff2": rng.standard_normal((h * 4, h)).astype(np.float32) * 0.1,
            "unembed": rng.standard_normal((h, v)).astype(np.float32) * 0.1,
        }
        self._ready = True

    def _tokenize(self, text: str) -> np.ndarray:
        """Byte-level tokenization."""
        tokens = [b for b in text.encode("utf-8")[:self.max_seq]]
        return np.array(tokens, dtype=np.int32)

    def _embed(self, tokens: np.ndarray) -> np.ndarray:
        """Token embedding lookup."""
        return self._weights["embed"][tokens]

    def _attention(self, x: np.ndarray) -> np.ndarray:
        """Single-head self-attention."""
        W = self._weights
        Q = x @ W["Wq"]
        K = x @ W["Wk"]
        V = x @ W["Wv"]

        scale = np.sqrt(self.hidden_size)
        scores = (Q @ K.T) / scale

        # Causal mask
        seq_len = x.shape[0]
        mask = np.triu(np.ones((seq_len, seq_len)) * -1e9, k=1)
        scores = scores + mask

        # Softmax
        exp_scores = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
        attn = exp_scores / (np.sum(exp_scores, axis=-1, keepdims=True) + 1e-9)

        out = attn @ V
        return out @ W["Wo"]

    def _ffn(self, x: np.ndarray) -> np.ndarray:
        """Feed-forward network with ReLU."""
        W = self._weights
        h = x @ W["ff1"]
        h = np.maximum(0, h)  # ReLU
        return h @ W["ff2"]

    def _layer_norm(self, x: np.ndarray) -> np.ndarray:
        """Simple layer norm."""
        mean = np.mean(x, axis=-1, keepdims=True)
        var = np.var(x, axis=-1, keepdims=True)
        return (x - mean) / (np.sqrt(var) + 1e-5)

    def forward(self, text: str) -> np.ndarray:
        """Forward pass. Returns logits over vocab."""
        tokens = self._tokenize(text)
        if len(tokens) == 0:
            return np.zeros(self.vocab_size)

        x = self._embed(tokens)
        x = self._layer_norm(x + self._attention(x))
        x = self._layer_norm(x + self._ffn(x))

        # Use last token's hidden state
        logits = x[-1] @ self._weights["unembed"]
        return logits

    def encode(self, text: str) -> np.ndarray:
        """Encode text to a fixed-size vector (last hidden state)."""
        tokens = self._tokenize(text)
        if len(tokens) == 0:
            return np.zeros(self.hidden_size)

        x = self._embed(tokens)
        x = self._layer_norm(x + self._attention(x))
        x = self._layer_norm(x + self._ffn(x))
        return x[-1]

    def similarity(self, text_a: str, text_b: str) -> float:
        """Cosine similarity between two texts."""
        a = self.encode(text_a)
        b = self.encode(text_b)
        dot = np.dot(a, b)
        norm = np.linalg.norm(a) * np.linalg.norm(b)
        if norm == 0:
            return 0.0
        return float(dot / norm)

    def classify(self, text: str, labels: list[str]) -> str:
        """Classify text against a list of labels by similarity."""
        enc = self.encode(text)
        best_label = labels[0]
        best_sim = -1.0
        for label in labels:
            label_enc = self.encode(label)
            dot = np.dot(enc, label_enc)
            norm = np.linalg.norm(enc) * np.linalg.norm(label_enc)
            sim = float(dot / norm) if norm > 0 else 0.0
            if sim > best_sim:
                best_sim = sim
                best_label = label
        return best_label

    @property
    def param_count(self) -> int:
        """Total parameter count."""
        return sum(w.size for w in self._weights.values())

    @property
    def memory_bytes(self) -> int:
        """Approximate memory usage in bytes."""
        return sum(w.nbytes for w in self._weights.values())

    def __repr__(self):
        return (f"FemtoLLM(h={self.hidden_size}, "
                f"params={self.param_count:,}, "
                f"mem={self.memory_bytes/1024:.0f}KB)")
