# eVGPU -- Electronic Virtual GPU

CPU-based AI/ML compute without GPU dependency. Uses numpy vectorization, BLAS, cache optimization, and threading. Operations: matmul(@), conv(*), pool, activate, grad.

## eVGPU Class

```python
"""
eVGPU — Electronic Virtual GPU.
CPU→AI/ML without GPU dependency.
Uses numpy vectorization, BLAS, cache optimization, threading.

Operations: matmul(@), conv(*), pool(↓), activate(σ), grad(∇)
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional
from concurrent.futures import ThreadPoolExecutor


@dataclass
class eVGPU:
    """Pure-CPU compute engine. No GPU needed."""
    cores: int = 4
    _executor: Optional[ThreadPoolExecutor] = field(default=None, repr=False)

    def __post_init__(self):
        self._executor = ThreadPoolExecutor(max_workers=self.cores)

    def tensor(self, a: np.ndarray, b: np.ndarray, op: str = "@") -> np.ndarray:
        """Core tensor operation. Uses numpy BLAS under the hood."""
        ops = {
            "@": lambda: np.matmul(a, b),
            "+": lambda: np.add(a, b),
            "*": lambda: np.multiply(a, b),
            "-": lambda: np.subtract(a, b),
        }
        if op not in ops:
            raise ValueError(f"Unknown op '{op}'. Use: {list(ops.keys())}")
        return ops[op]()

    def conv1d(self, signal: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        """1D convolution via numpy."""
        return np.convolve(signal, kernel, mode="same")

    def pool(self, x: np.ndarray, size: int = 2, mode: str = "max") -> np.ndarray:
        """Pooling operation (1D). Reduces dimensionality."""
        n = len(x)
        pooled_len = n // size
        reshaped = x[:pooled_len * size].reshape(pooled_len, size)
        if mode == "max":
            return reshaped.max(axis=1)
        elif mode == "avg":
            return reshaped.mean(axis=1)
        raise ValueError(f"Unknown pool mode '{mode}'. Use: max, avg")

    def activate(self, x: np.ndarray, fn: str = "relu") -> np.ndarray:
        """Activation functions."""
        fns = {
            "relu": lambda: np.maximum(0, x),
            "sigmoid": lambda: 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500))),
            "tanh": lambda: np.tanh(x),
            "softmax": lambda: _softmax(x),
        }
        if fn not in fns:
            raise ValueError(f"Unknown activation '{fn}'. Use: {list(fns.keys())}")
        return fns[fn]()

    def grad(self, x: np.ndarray, fn: str = "relu") -> np.ndarray:
        """Activation gradients for backprop."""
        grads = {
            "relu": lambda: (x > 0).astype(float),
            "sigmoid": lambda: _sig(x) * (1 - _sig(x)),
            "tanh": lambda: 1 - np.tanh(x) ** 2,
        }
        if fn not in grads:
            raise ValueError(f"No gradient for '{fn}'")
        return grads[fn]()

    def norm(self, x: np.ndarray, axis: int = -1,
             eps: float = 1e-5) -> np.ndarray:
        """Layer normalization."""
        mean = np.mean(x, axis=axis, keepdims=True)
        var = np.var(x, axis=axis, keepdims=True)
        return (x - mean) / np.sqrt(var + eps)

    def parallel_matmul(self, pairs: list) -> list:
        """Run multiple matmuls in parallel across CPU cores."""
        def _mm(pair):
            return np.matmul(pair[0], pair[1])
        return list(self._executor.map(_mm, pairs))
```

## Benchmark and Utilities

```python
    def benchmark(self, size: int = 256, iterations: int = 100) -> dict:
        """Benchmark CPU compute speed."""
        import time
        a = np.random.randn(size, size).astype(np.float32)
        b = np.random.randn(size, size).astype(np.float32)
        start = time.time()
        for _ in range(iterations):
            np.matmul(a, b)
        elapsed = time.time() - start
        flops = 2 * size**3 * iterations
        return {
            "matrix_size": size,
            "iterations": iterations,
            "elapsed_s": round(elapsed, 3),
            "gflops": round(flops / elapsed / 1e9, 2),
        }

    def shutdown(self):
        """Clean up thread pool."""
        if self._executor:
            self._executor.shutdown(wait=False)


def _softmax(x):
    e = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e / np.sum(e, axis=-1, keepdims=True)


def _sig(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))
```
