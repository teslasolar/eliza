# ISA-88 Procedural Control Model

Procedural hierarchy: Procedure -> UnitProcedure -> Operation -> Phase. Each level can specify ordering (Sequential, Parallel, or Mixed) to control how its children execute.

```python
"""
ISA-88 Procedural Control Model.

Hierarchy: Procedure -> UnitProcedure -> Operation -> Phase

Each level can specify ordering (Sequential, Parallel, or Mixed)
to control how its children execute.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Any
```

## Enums

```python
class Ordering(Enum):
    """Execution ordering of child procedural elements."""
    SEQUENTIAL = "Sequential"
    PARALLEL = "Parallel"
    MIXED = "Mixed"


class ParamType(Enum):
    """Phase parameter data types."""
    REAL = "REAL"
    INT = "INT"
    BOOL = "BOOL"
    STRING = "STRING"
    ENUM = "ENUM"


class PhaseState(Enum):
    """Current state of a phase instance (mirrors states.py enum)."""
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    HOLDING = "HOLDING"
    HELD = "HELD"
    RESTARTING = "RESTARTING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    ABORTING = "ABORTING"
    ABORTED = "ABORTED"
```

## Phase Parameter Definition

```python
@dataclass
class PhaseParam:
    """Definition of a configurable phase parameter."""
    name: str
    type: ParamType = ParamType.REAL
    default: Any = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    uom: str = ""
    desc: str = ""

    def validate(self, value: Any) -> Optional[str]:
        """Validate a value against this parameter spec."""
        if value is None:
            return None
        if self.type == ParamType.REAL or self.type == ParamType.INT:
            try:
                num = float(value)
            except (TypeError, ValueError):
                return f"{self.name}: cannot convert {value!r} to number"
            if self.min_value is not None and num < self.min_value:
                return f"{self.name}: {num} below min {self.min_value}"
            if self.max_value is not None and num > self.max_value:
                return f"{self.name}: {num} above max {self.max_value}"
        return None
```

## Procedural Elements

From the lowest level (Phase) up to the top (Procedure).

```python
@dataclass
class Phase:
    """The lowest procedural element — executes a single action.

    Attributes:
        id:        unique phase identifier
        name:      human-readable name
        logic_ref: reference to the control logic implementation
        params:    configurable parameters for this phase
        state:     current execution state
    """
    id: str
    name: str
    logic_ref: str = ""
    params: List[PhaseParam] = field(default_factory=list)
    state: PhaseState = PhaseState.IDLE

    def add_param(self, name: str, **kw) -> "Phase":
        self.params.append(PhaseParam(name=name, **kw))
        return self

    def validate_params(self, values: dict) -> List[str]:
        """Validate a dict of parameter values."""
        errors = []
        for p in self.params:
            v = values.get(p.name, p.default)
            err = p.validate(v)
            if err:
                errors.append(err)
        return errors

    def describe(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "logic_ref": self.logic_ref,
            "params": [p.name for p in self.params],
            "state": self.state.value,
        }

    def __repr__(self):
        return f"Phase({self.id}, {self.name}, state={self.state.value})"


@dataclass
class Operation:
    """A group of phases that accomplish a major processing action."""
    id: str
    name: str = ""
    phases: List[Phase] = field(default_factory=list)
    ordering: Ordering = Ordering.SEQUENTIAL

    def add_phase(self, phase: Phase) -> "Operation":
        self.phases.append(phase)
        return self

    def describe(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "ordering": self.ordering.value,
            "phases": [p.describe() for p in self.phases],
        }

    def __repr__(self):
        return (f"Operation({self.id}, {self.name}, "
                f"phases={len(self.phases)})")


@dataclass
class UnitProcedure:
    """A sequence of operations executed on a single unit."""
    id: str
    name: str = ""
    unit_class: str = ""        # required equipment class
    operations: List[Operation] = field(default_factory=list)
    ordering: Ordering = Ordering.SEQUENTIAL

    def add_operation(self, op: Operation) -> "UnitProcedure":
        self.operations.append(op)
        return self

    def describe(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "unit_class": self.unit_class,
            "ordering": self.ordering.value,
            "operations": [o.describe() for o in self.operations],
        }

    def __repr__(self):
        return (f"UnitProcedure({self.id}, {self.name}, "
                f"ops={len(self.operations)})")


@dataclass
class Procedure:
    """Top-level procedural element — the strategy for a batch.

    Contains one or more unit procedures that may execute
    sequentially, in parallel, or in a mixed order.
    """
    id: str
    name: str = ""
    unit_procedures: List[UnitProcedure] = field(default_factory=list)
    ordering: Ordering = Ordering.SEQUENTIAL

    def add_unit_procedure(self, up: UnitProcedure) -> "Procedure":
        self.unit_procedures.append(up)
        return self

    def describe(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "ordering": self.ordering.value,
            "unit_procedures": [
                up.describe() for up in self.unit_procedures
            ],
        }

    def __repr__(self):
        return (f"Procedure({self.id}, {self.name}, "
                f"unit_procs={len(self.unit_procedures)})")
```
