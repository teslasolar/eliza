"""
ISA-88 Batch Management — runtime batch tracking.

A Batch ties together a recipe, control recipe, unit allocations,
runtime parameters, and an event log that records the full history.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Any

from konomi.base import Timestamp


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class BatchState(Enum):
    """Batch lifecycle states (mirrors the batch state machine)."""
    CREATED = "Created"
    SCHEDULED = "Scheduled"
    RUNNING = "Running"
    COMPLETE = "Complete"
    HELD = "Held"
    ABORTED = "Aborted"


class BatchEventType(Enum):
    """Types of events recorded during batch execution."""
    STATE_CHANGE = "StateChange"
    PHASE_START = "PhaseStart"
    PHASE_COMPLETE = "PhaseComplete"
    PHASE_ABORT = "PhaseAbort"
    UNIT_ALLOCATED = "UnitAllocated"
    UNIT_RELEASED = "UnitReleased"
    PARAM_SET = "ParamSet"
    MATERIAL_ADDED = "MaterialAdded"
    ALARM = "Alarm"
    OPERATOR = "Operator"
    COMMENT = "Comment"


# ---------------------------------------------------------------------------
# Supporting dataclasses
# ---------------------------------------------------------------------------

@dataclass
class UnitAllocation:
    """Records which unit was allocated to a batch and when."""
    unit_id: str
    start: Timestamp
    end: Optional[Timestamp] = None

    @property
    def is_active(self) -> bool:
        return self.end is None

    @property
    def duration_seconds(self) -> Optional[float]:
        if self.end is None:
            return None
        return self.end.value - self.start.value


@dataclass
class BatchEvent:
    """A timestamped event in the batch history."""
    timestamp: Timestamp
    type: BatchEventType
    description: str
    phase_ref: Optional[str] = None
    data: dict = field(default_factory=dict)

    def __repr__(self):
        return (f"BatchEvent({self.type.value}, "
                f"{self.timestamp.iso8601}: {self.description})")


# ---------------------------------------------------------------------------
# Batch
# ---------------------------------------------------------------------------

@dataclass
class Batch:
    """ISA-88 Batch — a runtime instance of a recipe execution.

    Attributes:
        id:                 unique batch identifier
        recipe_id:          reference to the master recipe
        control_recipe_id:  reference to the control recipe (runtime copy)
        state:              current batch lifecycle state
        start:              batch start timestamp
        end:                batch end timestamp (None while running)
        unit_allocations:   history of unit allocations
        params:             runtime parameter overrides
        events:             ordered list of batch events
        product:            product being produced
        lot:                lot/batch number
    """
    id: str
    recipe_id: str
    control_recipe_id: Optional[str] = None
    state: BatchState = BatchState.CREATED
    start: Optional[Timestamp] = None
    end: Optional[Timestamp] = None
    unit_allocations: List[UnitAllocation] = field(default_factory=list)
    params: dict = field(default_factory=dict)
    events: List[BatchEvent] = field(default_factory=list)
    product: str = ""
    lot: str = ""

    # -- State transitions ---------------------------------------------------

    def schedule(self):
        """Move batch from CREATED to SCHEDULED."""
        self._require_state(BatchState.CREATED)
        self.state = BatchState.SCHEDULED
        self._log(BatchEventType.STATE_CHANGE, "Batch scheduled")

    def run(self):
        """Move batch from SCHEDULED to RUNNING."""
        self._require_state(BatchState.SCHEDULED)
        self.state = BatchState.RUNNING
        self.start = Timestamp.now()
        self._log(BatchEventType.STATE_CHANGE, "Batch started")

    def complete(self):
        """Move batch from RUNNING to COMPLETE."""
        self._require_state(BatchState.RUNNING)
        self.state = BatchState.COMPLETE
        self.end = Timestamp.now()
        self._release_all_units()
        self._log(BatchEventType.STATE_CHANGE, "Batch complete")

    def hold(self):
        """Move batch from RUNNING to HELD."""
        self._require_state(BatchState.RUNNING)
        self.state = BatchState.HELD
        self._log(BatchEventType.STATE_CHANGE, "Batch held")

    def restart(self):
        """Move batch from HELD to RUNNING."""
        self._require_state(BatchState.HELD)
        self.state = BatchState.RUNNING
        self._log(BatchEventType.STATE_CHANGE, "Batch restarted")

    def abort(self):
        """Move batch to ABORTED from RUNNING or HELD."""
        if self.state not in (BatchState.RUNNING, BatchState.HELD):
            raise ValueError(
                f"Cannot abort from {self.state.value}")
        self.state = BatchState.ABORTED
        self.end = Timestamp.now()
        self._release_all_units()
        self._log(BatchEventType.STATE_CHANGE, "Batch aborted")

    # -- Unit allocation -----------------------------------------------------

    def allocate_unit(self, unit_id: str):
        """Record a unit allocation."""
        alloc = UnitAllocation(unit_id=unit_id, start=Timestamp.now())
        self.unit_allocations.append(alloc)
        self._log(BatchEventType.UNIT_ALLOCATED,
                  f"Unit {unit_id} allocated")

    def release_unit(self, unit_id: str):
        """Release a previously allocated unit."""
        for alloc in self.unit_allocations:
            if alloc.unit_id == unit_id and alloc.is_active:
                alloc.end = Timestamp.now()
                self._log(BatchEventType.UNIT_RELEASED,
                          f"Unit {unit_id} released")
                return
        raise ValueError(f"No active allocation for unit {unit_id}")

    # -- Event logging -------------------------------------------------------

    def log_event(self, event_type: BatchEventType,
                  description: str, phase_ref: str = None,
                  **data):
        """Append a custom event to the batch history."""
        self._log(event_type, description, phase_ref, data)

    # -- Query ---------------------------------------------------------------

    @property
    def active_units(self) -> List[str]:
        return [a.unit_id for a in self.unit_allocations if a.is_active]

    @property
    def is_terminal(self) -> bool:
        return self.state in (BatchState.COMPLETE, BatchState.ABORTED)

    @property
    def duration_seconds(self) -> Optional[float]:
        if self.start is None:
            return None
        end = self.end or Timestamp.now()
        return end.value - self.start.value

    def events_of_type(self, etype: BatchEventType) -> List[BatchEvent]:
        return [e for e in self.events if e.type == etype]

    def describe(self) -> dict:
        return {
            "id": self.id,
            "recipe_id": self.recipe_id,
            "state": self.state.value,
            "product": self.product,
            "lot": self.lot,
            "start": str(self.start) if self.start else None,
            "end": str(self.end) if self.end else None,
            "active_units": self.active_units,
            "event_count": len(self.events),
        }

    def __repr__(self):
        return (f"Batch({self.id}, recipe={self.recipe_id}, "
                f"state={self.state.value})")

    # -- Internal helpers ----------------------------------------------------

    def _require_state(self, expected: BatchState):
        if self.state != expected:
            raise ValueError(
                f"Expected state {expected.value}, "
                f"got {self.state.value}")

    def _release_all_units(self):
        now = Timestamp.now()
        for alloc in self.unit_allocations:
            if alloc.is_active:
                alloc.end = now

    def _log(self, etype: BatchEventType, desc: str,
             phase_ref: str = None, data: dict = None):
        self.events.append(BatchEvent(
            timestamp=Timestamp.now(),
            type=etype,
            description=desc,
            phase_ref=phase_ref,
            data=data or {},
        ))
