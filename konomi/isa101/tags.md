# ISA-101 HMI Design Tags

Tag provider for ISA-101 HMI design. Exposes HMI navigation state, active layer, element counts, and display performance metrics.

```python
"""
ISA-101 Tag Provider — Ignition-style tags for HMI design.

Exposes HMI navigation state, active layer, element counts,
and display performance metrics.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class ISA101TagProvider(TagProvider):
    """Tag provider for ISA-101 HMI Design."""

    def __init__(self):
        super().__init__(prefix="ISA101")
        self.register(Tag(path="Active_Layer", type=TagType.STRING,
                          desc="Currently displayed HMI layer (L1-L4)"))
        self.register(Tag(path="Active_Screen", type=TagType.STRING,
                          desc="Currently displayed screen name"))
        self.register(Tag(path="Faceplate_Count", type=TagType.INTEGER,
                          desc="Total defined faceplates"))
        self.register(Tag(path="Trend_Count", type=TagType.INTEGER,
                          desc="Active trend displays"))
        self.register(Tag(path="Element_Count", type=TagType.INTEGER,
                          desc="Total graphic elements"))
        self.register(Tag(path="Navigation_Depth", type=TagType.INTEGER,
                          desc="Current drill-down depth"))
        self.register(Tag(path="Refresh_Rate_Ms", type=TagType.ANALOG,
                          desc="Screen refresh rate", unit="ms"))
        self.register(Tag(path="Color_Violations", type=TagType.INTEGER,
                          desc="Elements violating ISA-101 color rules"))
        # Defaults
        self.get("ISA101_Active_Layer").write("L1")
        self.get("ISA101_Navigation_Depth").write(0)
        self.get("ISA101_Refresh_Rate_Ms").write(1000.0)


def create_provider() -> ISA101TagProvider:
    return ISA101TagProvider()
```
