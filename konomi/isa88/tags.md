# ISA-88 Batch Control Tags

Tag provider for ISA-88 batch control. Exposes batch state, active procedures, equipment status, recipe counts, and phase execution metrics.

```python
"""
ISA-88 Tag Provider — Ignition-style tags for batch control.

Exposes batch state, active procedures, equipment status,
recipe counts, and phase execution metrics.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class ISA88TagProvider(TagProvider):
    """Tag provider for ISA-88 Batch Control."""

    def __init__(self):
        super().__init__(prefix="ISA88")
        # Batch runtime
        self.register(Tag(path="Active_Batches", type=TagType.INTEGER,
                          desc="Currently running batches"))
        self.register(Tag(path="Batch_State", type=TagType.STRING,
                          desc="Current batch state (IDLE/RUNNING/COMPLETE/HELD)"))
        self.register(Tag(path="Batch_ID", type=TagType.STRING,
                          desc="Active batch identifier"))
        # Procedures
        self.register(Tag(path="Active_Phase", type=TagType.STRING,
                          desc="Currently executing phase name"))
        self.register(Tag(path="Phase_Step", type=TagType.INTEGER,
                          desc="Current step within active phase"))
        self.register(Tag(path="Procedure_Count", type=TagType.INTEGER,
                          desc="Total defined procedures"))
        # Equipment
        self.register(Tag(path="Units_Available", type=TagType.INTEGER,
                          desc="Equipment units available for allocation"))
        self.register(Tag(path="Units_Allocated", type=TagType.INTEGER,
                          desc="Equipment units currently allocated"))
        # Recipes
        self.register(Tag(path="Recipe_Count", type=TagType.INTEGER,
                          desc="Total defined recipes"))
        self.register(Tag(path="Active_Recipe", type=TagType.STRING,
                          desc="Currently executing recipe name"))
        # State machine
        self.register(Tag(path="SM_Current_State", type=TagType.STRING,
                          desc="PackML state machine current state"))
        self.register(Tag(path="SM_Transitions", type=TagType.INTEGER,
                          desc="Total state transitions executed"))
        # Defaults
        self.get("ISA88_Batch_State").write("IDLE")
        self.get("ISA88_Active_Batches").write(0)
        self.get("ISA88_SM_Current_State").write("IDLE")


def create_provider() -> ISA88TagProvider:
    return ISA88TagProvider()
```
