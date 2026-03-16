# ISA-95 Process Segment Model

A `ProcessSegment` defines a step in a manufacturing process, specifying the required equipment, personnel, input/output materials, parameters, and expected duration.

```python
"""
ISA-95 Process Segment Model.

A ProcessSegment defines a step in a manufacturing process, specifying the
required equipment, personnel, input/output materials, parameters, and
expected duration.
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional

from konomi.base import Duration
```

## Supporting Dataclasses

```python
@dataclass
class ProcessParameter:
    """A named parameter for a process segment."""
    name: str
    value: Any = None
    uom: str = ""

    def __repr__(self) -> str:
        uom = f" {self.uom}" if self.uom else ""
        return f"ProcessParameter({self.name}={self.value}{uom})"


@dataclass
class MaterialRef:
    """A reference to a material used in a process segment."""
    material_id: str
    quantity: float = 0.0
    uom: str = ""
    role: str = ""  # e.g. "raw", "intermediate", "finished"

    def __repr__(self) -> str:
        return f"MaterialRef({self.material_id}, qty={self.quantity} {self.uom})"
```

## ProcessSegment

```python
@dataclass
class ProcessSegment:
    """
    A segment of a manufacturing process.

    Defines what equipment, personnel, materials, and parameters are
    needed, plus the expected duration.
    """
    id: str
    name: str
    desc: str = ""
    equipment_refs: List[str] = field(default_factory=list)
    personnel_refs: List[str] = field(default_factory=list)
    materials_in: List[MaterialRef] = field(default_factory=list)
    materials_out: List[MaterialRef] = field(default_factory=list)
    params: List[ProcessParameter] = field(default_factory=list)
    duration: Optional[Duration] = None

    def add_equipment(self, equipment_id: str) -> None:
        """Add an equipment reference."""
        if equipment_id not in self.equipment_refs:
            self.equipment_refs.append(equipment_id)

    def add_personnel(self, personnel_id: str) -> None:
        """Add a personnel reference."""
        if personnel_id not in self.personnel_refs:
            self.personnel_refs.append(personnel_id)

    def add_material_in(
        self,
        material_id: str,
        quantity: float = 0.0,
        uom: str = "",
        role: str = "raw",
    ) -> MaterialRef:
        """Add an input material reference."""
        ref = MaterialRef(
            material_id=material_id, quantity=quantity, uom=uom, role=role
        )
        self.materials_in.append(ref)
        return ref

    def add_material_out(
        self,
        material_id: str,
        quantity: float = 0.0,
        uom: str = "",
        role: str = "finished",
    ) -> MaterialRef:
        """Add an output material reference."""
        ref = MaterialRef(
            material_id=material_id, quantity=quantity, uom=uom, role=role
        )
        self.materials_out.append(ref)
        return ref

    def add_param(
        self, name: str, value: Any = None, uom: str = ""
    ) -> ProcessParameter:
        """Add a process parameter."""
        p = ProcessParameter(name=name, value=value, uom=uom)
        self.params.append(p)
        return p

    def __repr__(self) -> str:
        return (
            f"ProcessSegment({self.id}, {self.name}, "
            f"equip={len(self.equipment_refs)}, "
            f"mat_in={len(self.materials_in)}, "
            f"mat_out={len(self.materials_out)})"
        )
```
