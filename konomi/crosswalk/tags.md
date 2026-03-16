# Cross-Standard Mapping Tags

Tag provider for cross-standard mappings. Exposes mapping counts, sync status, and conflict detection.

```python
"""
Crosswalk Tag Provider — Ignition-style tags for cross-standard mappings.

Exposes mapping counts, sync status, and conflict detection.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class CrosswalkTagProvider(TagProvider):
    """Tag provider for cross-standard mappings."""

    def __init__(self):
        super().__init__(prefix="XWALK")
        self.register(Tag(path="Mapping_Count", type=TagType.INTEGER,
                          desc="Total cross-standard mappings"))
        self.register(Tag(path="Standards_Linked", type=TagType.INTEGER,
                          desc="Number of standards with active mappings"))
        self.register(Tag(path="Conflicts", type=TagType.INTEGER,
                          desc="Detected mapping conflicts"))
        self.register(Tag(path="Last_Sync", type=TagType.STRING,
                          desc="Last crosswalk synchronization timestamp"))
        self.register(Tag(path="Coverage_Pct", type=TagType.ANALOG,
                          desc="Percentage of entities with mappings", unit="%"))
        # Defaults
        self.get("XWALK_Standards_Linked").write(4)
        self.get("XWALK_Conflicts").write(0)


def create_provider() -> CrosswalkTagProvider:
    return CrosswalkTagProvider()
```
