# Crosswalk Mappings

Cross-standard mappings between industrial standards. Defines how entities in one standard map to entities in another.

## Core Types

```python
"""
Crosswalk mappings between standards.
How entities in one standard map to entities in another.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Callable


class MappingType(Enum):
    EXACT = "exact"          # 1:1 direct mapping
    PARTIAL = "partial"      # some fields map, others don't
    SEMANTIC = "semantic"    # conceptually similar, different structure


@dataclass
class CrosswalkEntry:
    """A single entity mapping between two standards."""
    from_std: str
    from_entity: str
    to_std: str
    to_entity: str
    mapping: MappingType = MappingType.EXACT
    transform: Optional[Callable] = None
    notes: str = ""

    def apply(self, data: dict) -> dict:
        """Transform data from source to target standard."""
        if self.transform:
            return self.transform(data)
        return data  # exact mapping = pass through

    def __repr__(self):
        return (f"{self.from_std}.{self.from_entity} "
                f"→[{self.mapping.value}]→ "
                f"{self.to_std}.{self.to_entity}")
```

## Crosswalk Registry

```python
class Crosswalk:
    """Registry of all cross-standard mappings."""

    def __init__(self):
        self.entries: list[CrosswalkEntry] = []

    def register(self, entry: CrosswalkEntry):
        self.entries.append(entry)

    def lookup(self, from_std: str, from_entity: str,
               to_std: str = None) -> list[CrosswalkEntry]:
        """Find mappings for an entity, optionally filtered by target."""
        results = []
        for e in self.entries:
            if e.from_std == from_std and e.from_entity == from_entity:
                if to_std is None or e.to_std == to_std:
                    results.append(e)
        return results

    def all_for_standard(self, std_id: str) -> list[CrosswalkEntry]:
        """Get all mappings involving a standard (as source or target)."""
        return [e for e in self.entries
                if e.from_std == std_id or e.to_std == std_id]
```

## Default Crosswalk Builder

```python
def build_default_crosswalks() -> Crosswalk:
    """Build the default set of cross-standard mappings."""
    cw = Crosswalk()

    # ISA-95 ↔ ISA-88
    for from_e, to_e in [
        ("WorkCenter", "ProcessCell"),
        ("WorkUnit", "Unit"),
        ("ProcessSegment", "Operation"),
    ]:
        cw.register(CrosswalkEntry("ISA-95", from_e, "ISA-88", to_e,
                                   MappingType.EXACT))

    cw.register(CrosswalkEntry(
        "ISA-95", "ProductionSchedule", "ISA-88", "Batch",
        MappingType.SEMANTIC,
        notes="Schedule instantiates as Batch"))

    # ISA-95 ↔ OPC-UA
    for from_e, to_e in [
        ("Equipment", "Object"),
        ("Property", "Variable"),
        ("Capability", "Method"),
    ]:
        cw.register(CrosswalkEntry("ISA-95", from_e, "OPC-UA", to_e,
                                   MappingType.PARTIAL,
                                   notes=f"ns=isa95"))

    # ISA-88 ↔ PackML
    for from_e, to_e in [
        ("PhaseState.RUNNING", "EXECUTE"),
        ("PhaseState.HELD", "HELD"),
        ("PhaseState.ABORTED", "ABORTED"),
    ]:
        cw.register(CrosswalkEntry("ISA-88", from_e, "PackML", to_e,
                                   MappingType.EXACT,
                                   notes="ISA-88 UnitState ≈ PackML subset"))

    # ISA-101 ↔ ISA-18.2
    for from_e, to_e, note in [
        ("AlarmIndicator", "AlarmState", "visual representation"),
        ("ColorMeaning.Alarm", "Priority", "color code mapping"),
        ("AlarmSummary", "AlarmList", "filter by area at L1-L5"),
    ]:
        cw.register(CrosswalkEntry("ISA-101", from_e, "ISA-18.2", to_e,
                                   MappingType.PARTIAL, notes=note))

    # OPC-UA ↔ Sparkplug
    for from_e, to_e in [
        ("Variable", "Metric"),
        ("Subscription", "NDATA/DDATA"),
        ("Method", "NCMD/DCMD"),
        ("AddressSpace", "NBIRTH"),
    ]:
        cw.register(CrosswalkEntry("OPC-UA", from_e, "Sparkplug", to_e,
                                   MappingType.SEMANTIC))

    return cw
```
