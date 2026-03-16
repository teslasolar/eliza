# ISA-18.2 Alarm Management Tags

Tag provider for ISA-18.2 alarm management. Exposes alarm counts by state and priority, alarm rate metrics, and shelving/suppression status.

```python
"""
ISA-18.2 Tag Provider — Ignition-style tags for alarm management.

Exposes alarm counts by state and priority, alarm rate metrics,
and shelving/suppression status.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class ISA18TagProvider(TagProvider):
    """Tag provider for ISA-18.2 Alarm Management."""

    def __init__(self):
        super().__init__(prefix="ISA18")
        # Alarm counts
        self.register(Tag(path="Active_Alarms", type=TagType.INTEGER,
                          desc="Currently active alarms"))
        self.register(Tag(path="Unacked_Alarms", type=TagType.INTEGER,
                          desc="Active alarms not yet acknowledged"))
        self.register(Tag(path="Shelved_Alarms", type=TagType.INTEGER,
                          desc="Alarms currently shelved"))
        self.register(Tag(path="Suppressed_Alarms", type=TagType.INTEGER,
                          desc="Alarms currently suppressed"))
        # Priority breakdown
        self.register(Tag(path="Critical_Count", type=TagType.INTEGER,
                          desc="Critical priority alarms active"))
        self.register(Tag(path="High_Count", type=TagType.INTEGER,
                          desc="High priority alarms active"))
        self.register(Tag(path="Medium_Count", type=TagType.INTEGER,
                          desc="Medium priority alarms active"))
        self.register(Tag(path="Low_Count", type=TagType.INTEGER,
                          desc="Low priority alarms active"))
        # Metrics
        self.register(Tag(path="Alarm_Rate", type=TagType.ANALOG,
                          desc="Alarms per 10 minutes", unit="alarms/10min"))
        self.register(Tag(path="Stale_Alarms", type=TagType.INTEGER,
                          desc="Alarms active > 24 hours (stale)"))
        self.register(Tag(path="Chattering_Count", type=TagType.INTEGER,
                          desc="Alarms with chattering behavior"))
        self.register(Tag(path="Flood_Active", type=TagType.DISCRETE,
                          desc="Alarm flood condition active"))
        # Defaults
        self.get("ISA18_Active_Alarms").write(0)
        self.get("ISA18_Flood_Active").write(False)


def create_provider() -> ISA18TagProvider:
    return ISA18TagProvider()
```
