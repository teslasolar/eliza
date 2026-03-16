# ISA-95 Data Flows

Information exchanged between hierarchy levels in the Purdue Reference Model. Defines what data types flow up and down between each pair of adjacent levels.

```python
"""
ISA-95 Data Flows — information exchanged between hierarchy levels.

Defines what data types flow up and down between each pair of adjacent
levels in the Purdue Reference Model.
"""

from dataclasses import dataclass, field
from typing import List
```

## DataFlow Dataclass

```python
@dataclass
class DataFlow:
    """A directional data flow between two ISA-95 levels."""
    from_level: int
    to_level: int
    data_types: List[str] = field(default_factory=list)
    desc: str = ""

    @property
    def direction(self) -> str:
        """Human-readable direction label."""
        if self.to_level > self.from_level:
            return "up"
        elif self.to_level < self.from_level:
            return "down"
        return "lateral"

    @property
    def label(self) -> str:
        return f"L{self.from_level} -> L{self.to_level}"

    def __repr__(self) -> str:
        return (
            f"DataFlow(L{self.from_level}->L{self.to_level}, "
            f"types={len(self.data_types)}, {self.direction})"
        )
```

## L4 <-> L3 (Business <-> MOM)

```python
FLOW_L4_L3 = DataFlow(
    from_level=4,
    to_level=3,
    data_types=[
        "ProductionSchedule",
        "MaterialDefinition",
        "ProductDefinition",
        "WorkOrder",
        "ResourceRequirements",
        "QualitySpecifications",
    ],
    desc="Business planning pushes schedules and definitions to MOM",
)

FLOW_L3_L4 = DataFlow(
    from_level=3,
    to_level=4,
    data_types=[
        "ProductionPerformance",
        "InventoryReport",
        "QualityResults",
        "ProductionStatus",
        "ResourceUtilization",
        "CostData",
    ],
    desc="MOM reports performance, inventory, and quality back to business",
)
```

## L3 <-> L2 (MOM <-> Control)

```python
FLOW_L3_L2 = DataFlow(
    from_level=3,
    to_level=2,
    data_types=[
        "Recipe",
        "Setpoints",
        "Commands",
        "Schedule",
        "BatchDirectives",
        "EquipmentParameters",
    ],
    desc="MOM sends recipes, setpoints, and commands to supervisory control",
)

FLOW_L2_L3 = DataFlow(
    from_level=2,
    to_level=3,
    data_types=[
        "ProcessData",
        "Events",
        "Alarms",
        "BatchRecord",
        "EquipmentStatus",
        "ProductionCounts",
    ],
    desc="Supervisory control reports process data and events to MOM",
)
```

## L2 <-> L1 (Control <-> Sensing)

```python
FLOW_L2_L1 = DataFlow(
    from_level=2,
    to_level=1,
    data_types=[
        "Setpoints",
        "Commands",
        "ControlParameters",
        "InterlockConfig",
    ],
    desc="Supervisory control sends setpoints and commands to direct control",
)

FLOW_L1_L2 = DataFlow(
    from_level=1,
    to_level=2,
    data_types=[
        "Measurements",
        "ControllerStatus",
        "Alarms",
        "InterlockStatus",
        "DiagnosticData",
    ],
    desc="Direct control reports measurements and status to supervisory",
)
```

## L1 <-> L0 (Sensing <-> Process)

```python
FLOW_L1_L0 = DataFlow(
    from_level=1,
    to_level=0,
    data_types=[
        "Setpoints",
        "Commands",
        "Calibration",
    ],
    desc="Direct control sends setpoints and commands to field devices",
)

FLOW_L0_L1 = DataFlow(
    from_level=0,
    to_level=1,
    data_types=[
        "Measurements",
        "RawSignals",
        "DeviceStatus",
    ],
    desc="Field devices report measurements and status to direct control",
)
```

## Aggregated Lists and Helpers

```python
ALL_FLOWS: List[DataFlow] = [
    FLOW_L4_L3,
    FLOW_L3_L4,
    FLOW_L3_L2,
    FLOW_L2_L3,
    FLOW_L2_L1,
    FLOW_L1_L2,
    FLOW_L1_L0,
    FLOW_L0_L1,
]

DOWNWARD_FLOWS: List[DataFlow] = [f for f in ALL_FLOWS if f.direction == "down"]
UPWARD_FLOWS: List[DataFlow] = [f for f in ALL_FLOWS if f.direction == "up"]


def flows_from(level: int) -> List[DataFlow]:
    """Return all flows originating from a given level."""
    return [f for f in ALL_FLOWS if f.from_level == level]


def flows_to(level: int) -> List[DataFlow]:
    """Return all flows arriving at a given level."""
    return [f for f in ALL_FLOWS if f.to_level == level]
```
