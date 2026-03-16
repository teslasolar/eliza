"""
Base Tag Provider — Ignition-style tags for primitive types layer.

Exposes system-level value infrastructure: timestamp precision,
quality distribution, active value count.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class BaseTagProvider(TagProvider):
    """Tag provider for base primitives."""

    def __init__(self):
        super().__init__(prefix="BASE")
        self.register(Tag(path="Timestamp_Format", type=TagType.STRING,
                          desc="Active timestamp format (ISO8601/EPOCH_MS)"))
        self.register(Tag(path="Quality_Good_Pct", type=TagType.ANALOG,
                          desc="Percentage of tags with GOOD quality", unit="%"))
        self.register(Tag(path="Quality_Bad_Count", type=TagType.INTEGER,
                          desc="Number of tags with BAD quality"))
        self.register(Tag(path="Active_Values", type=TagType.INTEGER,
                          desc="Number of values currently held"))
        self.register(Tag(path="Range_Violations", type=TagType.INTEGER,
                          desc="Values outside their defined range"))
        # Defaults
        self.get("BASE_Timestamp_Format").write("ISO8601")
        self.get("BASE_Quality_Good_Pct").write(100.0)
        self.get("BASE_Quality_Bad_Count").write(0)


def create_provider() -> BaseTagProvider:
    return BaseTagProvider()
