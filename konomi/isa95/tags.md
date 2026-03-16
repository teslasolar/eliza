# ISA-95 Enterprise/Control Integration Tags

Tag provider for ISA-95 enterprise/control integration. Exposes Purdue level activity, equipment states, material tracking, personnel status, and production KPIs.

```python
"""
ISA-95 Tag Provider — Ignition-style tags for enterprise/control integration.

Exposes Purdue level activity, equipment states, material tracking,
personnel status, and production KPIs.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class ISA95TagProvider(TagProvider):
    """Tag provider for ISA-95."""

    def __init__(self):
        super().__init__(prefix="ISA95")
        # Levels
        self.register(Tag(path="Active_Level", type=TagType.STRING,
                          desc="Most active Purdue hierarchy level"))
        self.register(Tag(path="L3_L2_Msg_Count", type=TagType.INTEGER,
                          desc="Messages flowing L3→L2"))
        self.register(Tag(path="L2_L3_Msg_Count", type=TagType.INTEGER,
                          desc="Messages flowing L2→L3"))
        # Equipment
        self.register(Tag(path="Equipment_Online", type=TagType.INTEGER,
                          desc="Equipment assets in ONLINE state"))
        self.register(Tag(path="Equipment_Offline", type=TagType.INTEGER,
                          desc="Equipment in maintenance/offline"))
        self.register(Tag(path="Equipment_Total", type=TagType.INTEGER,
                          desc="Total registered equipment"))
        # Material
        self.register(Tag(path="Material_Classes", type=TagType.INTEGER,
                          desc="Defined material classes"))
        self.register(Tag(path="Active_Lots", type=TagType.INTEGER,
                          desc="Material lots currently in process"))
        # Personnel
        self.register(Tag(path="Personnel_OnShift", type=TagType.INTEGER,
                          desc="Personnel currently on shift"))
        self.register(Tag(path="Qualified_Ops", type=TagType.INTEGER,
                          desc="Operators with active qualifications"))
        # Production
        self.register(Tag(path="Schedule_State", type=TagType.STRING,
                          desc="Production schedule state"))
        self.register(Tag(path="Segments_Complete", type=TagType.INTEGER,
                          desc="Production segments completed"))
        # Defaults
        self.get("ISA95_Active_Level").write("L3")
        self.get("ISA95_Schedule_State").write("RELEASED")


def create_provider() -> ISA95TagProvider:
    return ISA95TagProvider()
```
