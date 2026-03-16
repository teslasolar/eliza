# ISA-95 Level Hierarchy

The 5-level Purdue Reference Model for manufacturing systems integration.

- L4: Business Planning & Logistics (ERP, BI)
- L3: Manufacturing Operations Management (MES, LIMS, WMS)
- L2: Monitoring, Supervisory Control (SCADA, HMI, Batch)
- L1: Sensing & Direct Control (PLC, DCS, RTU)
- L0: Physical Process (Sensors, Actuators)

```python
"""
ISA-95 Level Hierarchy — the 5-level Purdue Reference Model.

L4: Business Planning & Logistics (ERP, BI)
L3: Manufacturing Operations Management (MES, LIMS, WMS)
L2: Monitoring, Supervisory Control (SCADA, HMI, Batch)
L1: Sensing & Direct Control (PLC, DCS, RTU)
L0: Physical Process (Sensors, Actuators)
"""

from dataclasses import dataclass, field
from typing import List
```

## Level Dataclass

```python
@dataclass
class Level:
    """A single level in the ISA-95 Purdue Reference Model."""
    id: int
    name: str
    scope: str
    timescale: str
    systems: List[str] = field(default_factory=list)
    data_down: List[str] = field(default_factory=list)
    data_up: List[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return f"L{self.id}: {self.name}"

    def __repr__(self) -> str:
        return f"Level(L{self.id}, {self.name}, timescale={self.timescale})"
```

## Level Instances

```python
L0 = Level(
    id=0,
    name="Process",
    scope="Physical process — sensors, actuators, field devices",
    timescale="continuous",
    systems=["Sensors", "Actuators", "Field Devices", "Instruments"],
    data_down=["Setpoints", "Commands", "Calibration"],
    data_up=["Measurements", "Raw Signals", "Device Status"],
)

L1 = Level(
    id=1,
    name="Sensing",
    scope="Direct control — PLCs, DCS controllers, RTUs",
    timescale="ms-sec",
    systems=["PLC", "DCS", "RTU", "Safety PLC"],
    data_down=["Setpoints", "Commands", "Recipes"],
    data_up=["Measurements", "Controller Status", "Alarms", "Interlocks"],
)

L2 = Level(
    id=2,
    name="Control",
    scope="Supervisory control — SCADA, HMI, Batch engines",
    timescale="sec-hours",
    systems=["SCADA", "HMI", "Batch Engine", "Historian"],
    data_down=["Recipes", "Schedules", "Setpoints", "Commands"],
    data_up=["Process Data", "Events", "Alarms", "Batch Records"],
)

L3 = Level(
    id=3,
    name="MOM",
    scope="Manufacturing Operations Management — MES, LIMS, WMS",
    timescale="shifts-days",
    systems=["MES", "LIMS", "WMS", "CMMS", "QMS"],
    data_down=["Work Orders", "Schedules", "Material Definitions", "Product Definitions"],
    data_up=["Performance", "Inventory", "Quality", "Production Status"],
)

L4 = Level(
    id=4,
    name="Business",
    scope="Business planning & logistics — ERP, BI, SCM",
    timescale="days-months",
    systems=["ERP", "BI", "SCM", "PLM", "CRM"],
    data_down=["Production Schedule", "Material Requirements", "Business Rules"],
    data_up=["Production Performance", "Inventory Reports", "KPIs", "Financials"],
)

# Ordered list of all levels (L0 at index 0)
ALL_LEVELS: List[Level] = [L0, L1, L2, L3, L4]
```

## Lookup Helper

```python
def get_level(level_id: int) -> Level:
    """Return the Level for a given numeric id (0-4)."""
    if 0 <= level_id <= 4:
        return ALL_LEVELS[level_id]
    raise ValueError(f"ISA-95 level must be 0-4, got {level_id}")
```
