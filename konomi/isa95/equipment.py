"""
ISA-95 Equipment Hierarchy & Physical Assets.

Hierarchy: Enterprise -> Site -> Area -> WorkCenter -> WorkUnit -> Equipment

Each piece of equipment has a state (operational condition) and a mode
(how it is being operated).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class EquipmentState(Enum):
    """Operational state of a piece of equipment."""
    IDLE = "Idle"
    RUNNING = "Running"
    FAULTED = "Faulted"
    MAINTENANCE = "Maintenance"
    OFFLINE = "Offline"


class EquipmentMode(Enum):
    """Operating mode of a piece of equipment."""
    PRODUCTION = "Production"
    MAINTENANCE = "Maintenance"
    MANUAL = "Manual"
    AUTOMATIC = "Automatic"
    SEMIAUTO = "Semiauto"


class HierarchyLevel(Enum):
    """Position within the ISA-95 equipment hierarchy."""
    ENTERPRISE = "Enterprise"
    SITE = "Site"
    AREA = "Area"
    WORK_CENTER = "WorkCenter"
    WORK_UNIT = "WorkUnit"
    EQUIPMENT = "Equipment"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class PhysicalAsset:
    """A physical asset in the ISA-95 equipment hierarchy."""
    id: str
    path: str
    name: str
    desc: str = ""
    level: HierarchyLevel = HierarchyLevel.EQUIPMENT
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)
    props: Dict[str, Any] = field(default_factory=dict)

    @property
    def full_path(self) -> str:
        """Return the hierarchical path including the asset name."""
        return f"{self.path}/{self.name}" if self.path else self.name

    def add_child(self, child_id: str) -> None:
        """Register a child asset id."""
        if child_id not in self.children:
            self.children.append(child_id)

    def set_prop(self, key: str, value: Any) -> None:
        """Set a property on this asset."""
        self.props[key] = value

    def get_prop(self, key: str, default: Any = None) -> Any:
        """Get a property value."""
        return self.props.get(key, default)

    def __repr__(self) -> str:
        return (
            f"PhysicalAsset({self.id}, {self.level.value}, "
            f"path={self.full_path})"
        )


@dataclass
class Equipment(PhysicalAsset):
    """
    An operational equipment entity extending PhysicalAsset with
    capability, state, and mode.
    """
    capability: str = ""
    state: EquipmentState = EquipmentState.IDLE
    mode: EquipmentMode = EquipmentMode.AUTOMATIC

    def is_available(self) -> bool:
        """True if equipment is idle and in production or automatic mode."""
        return (
            self.state == EquipmentState.IDLE
            and self.mode in (EquipmentMode.PRODUCTION, EquipmentMode.AUTOMATIC)
        )

    def start(self) -> None:
        """Transition to RUNNING state."""
        if self.state == EquipmentState.FAULTED:
            raise RuntimeError(f"Cannot start faulted equipment {self.id}")
        self.state = EquipmentState.RUNNING

    def stop(self) -> None:
        """Transition to IDLE state."""
        self.state = EquipmentState.IDLE

    def fault(self) -> None:
        """Transition to FAULTED state."""
        self.state = EquipmentState.FAULTED

    def set_maintenance(self) -> None:
        """Put equipment into maintenance."""
        self.state = EquipmentState.MAINTENANCE
        self.mode = EquipmentMode.MAINTENANCE

    def __repr__(self) -> str:
        return (
            f"Equipment({self.id}, {self.state.value}, "
            f"mode={self.mode.value}, cap={self.capability})"
        )
