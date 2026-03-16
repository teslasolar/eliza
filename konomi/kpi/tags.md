# KPI Performance Metrics Tags

Tag provider for KPI performance metrics. Exposes OEE components, reliability metrics, cycle time, throughput, and energy consumption.

```python
"""
KPI Tag Provider — Ignition-style tags for performance metrics.

Exposes OEE components, reliability metrics, cycle time,
throughput, and energy consumption.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class KPITagProvider(TagProvider):
    """Tag provider for KPI metrics."""

    def __init__(self):
        super().__init__(prefix="KPI")
        # OEE
        self.register(Tag(path="OEE_Overall", type=TagType.ANALOG,
                          desc="Overall Equipment Effectiveness", unit="%"))
        self.register(Tag(path="OEE_Availability", type=TagType.ANALOG,
                          desc="OEE availability component", unit="%"))
        self.register(Tag(path="OEE_Performance", type=TagType.ANALOG,
                          desc="OEE performance component", unit="%"))
        self.register(Tag(path="OEE_Quality", type=TagType.ANALOG,
                          desc="OEE quality component", unit="%"))
        # Reliability
        self.register(Tag(path="MTBF_Hours", type=TagType.ANALOG,
                          desc="Mean Time Between Failures", unit="hours"))
        self.register(Tag(path="MTTR_Hours", type=TagType.ANALOG,
                          desc="Mean Time To Repair", unit="hours"))
        # Production
        self.register(Tag(path="Cycle_Time_Sec", type=TagType.ANALOG,
                          desc="Average cycle time", unit="seconds"))
        self.register(Tag(path="Throughput", type=TagType.ANALOG,
                          desc="Units per hour", unit="units/hr"))
        self.register(Tag(path="First_Pass_Yield", type=TagType.ANALOG,
                          desc="First pass yield rate", unit="%"))
        # Energy
        self.register(Tag(path="Energy_KWh", type=TagType.ANALOG,
                          desc="Energy consumption", unit="kWh"))
        self.register(Tag(path="Energy_Per_Unit", type=TagType.ANALOG,
                          desc="Energy per unit produced", unit="kWh/unit"))
        # Defaults
        self.get("KPI_OEE_Overall").write(85.0)


def create_provider() -> KPITagProvider:
    return KPITagProvider()
```
