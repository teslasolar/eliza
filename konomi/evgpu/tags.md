# eVGPU Compute Engine Tags

Tag provider for the eVGPU CPU-based compute engine. Exposes core count, GFLOPS, tensor operations, utilization, and benchmark results.

```python
"""
eVGPU Tag Provider — Ignition-style tags for CPU-based compute.

Exposes core count, GFLOPS, tensor operations, utilization,
and benchmark results.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class EVGPUTagProvider(TagProvider):
    """Tag provider for the eVGPU compute engine."""

    def __init__(self):
        super().__init__(prefix="EVGPU")
        self.register(Tag(path="Cores", type=TagType.INTEGER,
                          desc="Number of compute cores"))
        self.register(Tag(path="GFLOPS", type=TagType.ANALOG,
                          desc="Last benchmark GFLOPS"))
        self.register(Tag(path="Utilization_Pct", type=TagType.ANALOG,
                          desc="Current core utilization", unit="%"))
        self.register(Tag(path="Tensor_Ops", type=TagType.INTEGER,
                          desc="Total tensor operations executed"))
        self.register(Tag(path="Active_Threads", type=TagType.INTEGER,
                          desc="Active compute threads"))
        self.register(Tag(path="Memory_MB", type=TagType.ANALOG,
                          desc="Memory usage", unit="MB"))
        self.register(Tag(path="Benchmark_Size", type=TagType.INTEGER,
                          desc="Last benchmark matrix size"))
        # Defaults
        self.get("EVGPU_Cores").write(4)
        self.get("EVGPU_Utilization_Pct").write(0.0)


def create_provider() -> EVGPUTagProvider:
    return EVGPUTagProvider()
```
