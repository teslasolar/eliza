# ISA-88 Equipment Hierarchy

Physical model for ISA-88 batch control. The hierarchy runs from Enterprise down to ControlModule: Enterprise -> Site -> Area -> ProcessCell -> Unit -> EquipmentModule -> ControlModule. Each level is a dataclass extending the base `Equipment` class.

```python
"""
ISA-88 Equipment Hierarchy — physical model.

Hierarchy: Enterprise -> Site -> Area -> ProcessCell -> Unit ->
           EquipmentModule -> ControlModule

Each level is a dataclass that extends the base Equipment class.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List

from konomi.base import Identifier
```

## Enums

```python
class EquipmentModuleType(Enum):
    """Common equipment module types in batch processing."""
    AGITATOR = "Agitator"
    HEATER = "Heater"
    COOLER = "Cooler"
    PUMP = "Pump"
    VALVE = "Valve"
    CONVEYOR = "Conveyor"
    WEIGH_SCALE = "WeighScale"
    SENSOR = "Sensor"
    DOSING = "Dosing"
    FILTER = "Filter"
    OTHER = "Other"


class ControlModuleType(Enum):
    """Control module I/O types."""
    ANALOG_INPUT = "AI"
    ANALOG_OUTPUT = "AO"
    DISCRETE_INPUT = "DI"
    DISCRETE_OUTPUT = "DO"
    MOTOR = "Motor"
    VALVE = "Valve"
    PID = "PID"
    TOTALIZER = "Totalizer"
    OTHER = "Other"


class UnitMode(Enum):
    """ISA-88 unit modes."""
    AUTOMATIC = "Automatic"
    SEMI_AUTOMATIC = "SemiAutomatic"
    MANUAL = "Manual"
    MAINTENANCE = "Maintenance"


class UnitState(Enum):
    """Simplified unit state for allocation tracking."""
    IDLE = "Idle"
    RUNNING = "Running"
    HELD = "Held"
    FAULTED = "Faulted"
    MAINTENANCE = "Maintenance"
```

## Base Equipment and IOTag

```python
@dataclass
class Equipment:
    """Base class for all ISA-88 equipment hierarchy levels."""
    id: str
    name: str
    desc: str = ""
    parent_id: Optional[str] = None
    properties: dict = field(default_factory=dict)

    def path(self) -> str:
        """Equipment path (parent/name)."""
        if self.parent_id:
            return f"{self.parent_id}/{self.name}"
        return self.name


@dataclass
class IOTag:
    """An I/O tag bound to a control module."""
    name: str
    address: str
    type: str = "REAL"        # REAL, BOOL, INT, STRING
    desc: str = ""
    eng_unit: str = ""
    range_lo: Optional[float] = None
    range_hi: Optional[float] = None
```

## Hierarchy Levels

From the lowest level (ControlModule) up to the top (Enterprise).

```python
@dataclass
class ControlModule(Equipment):
    """Lowest equipment level — handles a single I/O function."""
    type: ControlModuleType = ControlModuleType.OTHER
    io_tags: List[IOTag] = field(default_factory=list)

    def add_tag(self, tag: IOTag) -> "ControlModule":
        self.io_tags.append(tag)
        return self


@dataclass
class EquipmentModule(Equipment):
    """Functional grouping of control modules (e.g. an agitator assembly)."""
    type: EquipmentModuleType = EquipmentModuleType.OTHER
    control_modules: List[ControlModule] = field(default_factory=list)

    def add_control_module(self, cm: ControlModule) -> "EquipmentModule":
        cm.parent_id = self.id
        self.control_modules.append(cm)
        return self


@dataclass
class Unit(Equipment):
    """A unit that can execute one batch at a time."""
    equipment_modules: List[EquipmentModule] = field(default_factory=list)
    state: UnitState = UnitState.IDLE
    mode: UnitMode = UnitMode.AUTOMATIC
    allocated_to: Optional[str] = None   # batch id or None

    def add_equipment_module(self, em: EquipmentModule) -> "Unit":
        em.parent_id = self.id
        self.equipment_modules.append(em)
        return self

    @property
    def is_available(self) -> bool:
        return self.allocated_to is None and self.state == UnitState.IDLE

    def allocate(self, batch_id: str):
        self.allocated_to = batch_id
        self.state = UnitState.RUNNING

    def release(self):
        self.allocated_to = None
        self.state = UnitState.IDLE


@dataclass
class ProcessCell(Equipment):
    """Contains units and coordinates batch execution."""
    units: List[Unit] = field(default_factory=list)
    coordination_control: Optional[str] = None   # reference to control logic

    def add_unit(self, unit: Unit) -> "ProcessCell":
        unit.parent_id = self.id
        self.units.append(unit)
        return self

    def available_units(self) -> List[Unit]:
        return [u for u in self.units if u.is_available]


@dataclass
class Area(Equipment):
    """A logical grouping of process cells within a site."""
    process_cells: List[ProcessCell] = field(default_factory=list)

    def add_process_cell(self, pc: ProcessCell) -> "Area":
        pc.parent_id = self.id
        self.process_cells.append(pc)
        return self


@dataclass
class Site(Equipment):
    """A physical plant or location."""
    areas: List[Area] = field(default_factory=list)

    def add_area(self, area: Area) -> "Site":
        area.parent_id = self.id
        self.areas.append(area)
        return self


@dataclass
class Enterprise(Equipment):
    """Top-level organizational entity."""
    sites: List[Site] = field(default_factory=list)

    def add_site(self, site: Site) -> "Enterprise":
        site.parent_id = self.id
        self.sites.append(site)
        return self
```
