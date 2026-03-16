"""
ISA-95 Production Scheduling & Performance.

ProductionSchedule defines planned work (work orders).
ProductionPerformance captures what actually happened.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from konomi.base import Timestamp


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ScheduleState(Enum):
    """Lifecycle state of a production schedule."""
    CREATED = "Created"
    SCHEDULED = "Scheduled"
    RUNNING = "Running"
    COMPLETE = "Complete"
    CANCELLED = "Cancelled"


# ---------------------------------------------------------------------------
# Supporting dataclasses
# ---------------------------------------------------------------------------

@dataclass
class SegmentRequirement:
    """A reference to a process segment within a schedule."""
    segment_id: str
    quantity: float = 0.0
    uom: str = ""
    equipment_ref: Optional[str] = None
    personnel_refs: List[str] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"SegmentRequirement({self.segment_id}, qty={self.quantity})"


@dataclass
class SegmentActual:
    """Actual execution data for a segment within a performance record."""
    segment_id: str
    actual_start: Optional[Timestamp] = None
    actual_end: Optional[Timestamp] = None
    quantity_produced: float = 0.0
    uom: str = ""
    equipment_ref: Optional[str] = None
    props: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration_seconds(self) -> Optional[float]:
        """Elapsed time in seconds, or None if start/end missing."""
        if self.actual_start and self.actual_end:
            return self.actual_end.value - self.actual_start.value
        return None

    def __repr__(self) -> str:
        return (
            f"SegmentActual({self.segment_id}, "
            f"qty={self.quantity_produced} {self.uom})"
        )


@dataclass
class KPI:
    """A key performance indicator attached to a performance record."""
    name: str
    value: float
    uom: str = ""
    target: Optional[float] = None

    @property
    def on_target(self) -> Optional[bool]:
        """True if value meets or exceeds target (when target is set)."""
        if self.target is not None:
            return self.value >= self.target
        return None

    def __repr__(self) -> str:
        tgt = f", target={self.target}" if self.target is not None else ""
        return f"KPI({self.name}={self.value} {self.uom}{tgt})"


# ---------------------------------------------------------------------------
# Core dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ProductionSchedule:
    """A production schedule / work order."""
    id: str
    start: Optional[Timestamp] = None
    end: Optional[Timestamp] = None
    segments: List[SegmentRequirement] = field(default_factory=list)
    priority: int = 0
    state: ScheduleState = ScheduleState.CREATED
    desc: str = ""

    def add_segment(
        self,
        segment_id: str,
        quantity: float = 0.0,
        uom: str = "",
        equipment_ref: Optional[str] = None,
    ) -> SegmentRequirement:
        """Add a segment requirement."""
        req = SegmentRequirement(
            segment_id=segment_id,
            quantity=quantity,
            uom=uom,
            equipment_ref=equipment_ref,
        )
        self.segments.append(req)
        return req

    def schedule(self) -> None:
        """Move to SCHEDULED state."""
        self.state = ScheduleState.SCHEDULED

    def run(self) -> None:
        """Move to RUNNING state."""
        self.state = ScheduleState.RUNNING

    def complete(self) -> None:
        """Move to COMPLETE state."""
        self.state = ScheduleState.COMPLETE

    def cancel(self) -> None:
        """Move to CANCELLED state."""
        self.state = ScheduleState.CANCELLED

    def __repr__(self) -> str:
        return (
            f"ProductionSchedule({self.id}, state={self.state.value}, "
            f"priority={self.priority}, segments={len(self.segments)})"
        )


@dataclass
class ProductionPerformance:
    """Actual production performance against a schedule."""
    id: str
    schedule_ref: Optional[str] = None
    actual_start: Optional[Timestamp] = None
    actual_end: Optional[Timestamp] = None
    segments: List[SegmentActual] = field(default_factory=list)
    kpis: List[KPI] = field(default_factory=list)

    def add_segment(
        self,
        segment_id: str,
        actual_start: Optional[Timestamp] = None,
        actual_end: Optional[Timestamp] = None,
        quantity_produced: float = 0.0,
        uom: str = "",
    ) -> SegmentActual:
        """Record actual data for a segment."""
        sa = SegmentActual(
            segment_id=segment_id,
            actual_start=actual_start,
            actual_end=actual_end,
            quantity_produced=quantity_produced,
            uom=uom,
        )
        self.segments.append(sa)
        return sa

    def add_kpi(
        self,
        name: str,
        value: float,
        uom: str = "",
        target: Optional[float] = None,
    ) -> KPI:
        """Add a KPI measurement."""
        kpi = KPI(name=name, value=value, uom=uom, target=target)
        self.kpis.append(kpi)
        return kpi

    @property
    def total_produced(self) -> float:
        """Sum of quantities produced across all segments."""
        return sum(s.quantity_produced for s in self.segments)

    def __repr__(self) -> str:
        return (
            f"ProductionPerformance({self.id}, "
            f"schedule={self.schedule_ref}, "
            f"segments={len(self.segments)}, kpis={len(self.kpis)})"
        )
