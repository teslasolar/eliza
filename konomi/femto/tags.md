# FemtoLLM Tiny ML Model Tags

Tag provider for FemtoLLM. Exposes model state, parameter count, memory usage, classification metrics, and inference latency.

```python
"""
FemtoLLM Tag Provider — Ignition-style tags for the tiny ML model.

Exposes model state, parameter count, memory usage,
classification metrics, and inference latency.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class FemtoTagProvider(TagProvider):
    """Tag provider for FemtoLLM."""

    def __init__(self):
        super().__init__(prefix="FEMTO")
        self.register(Tag(path="Model_Loaded", type=TagType.DISCRETE,
                          desc="FemtoLLM model loaded"))
        self.register(Tag(path="Param_Count", type=TagType.INTEGER,
                          desc="Total model parameters"))
        self.register(Tag(path="Memory_KB", type=TagType.ANALOG,
                          desc="Model memory footprint", unit="KB"))
        self.register(Tag(path="Inferences", type=TagType.INTEGER,
                          desc="Total classification inferences"))
        self.register(Tag(path="Latency_Ms", type=TagType.ANALOG,
                          desc="Average inference latency", unit="ms"))
        self.register(Tag(path="Last_Label", type=TagType.STRING,
                          desc="Last classification result"))
        self.register(Tag(path="Confidence", type=TagType.ANALOG,
                          desc="Last classification confidence", unit="%"))
        # Defaults
        self.get("FEMTO_Model_Loaded").write(False)
        self.get("FEMTO_Inferences").write(0)


def create_provider() -> FemtoTagProvider:
    return FemtoTagProvider()
```
