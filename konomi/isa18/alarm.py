"""
ISA-18.2 Alarm and AlarmClass — the core alarm UDTs.

An Alarm is a single configured alarm point.
An AlarmClass groups alarms that share priority, sound, and behaviour.
"""

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Alarm types
# ---------------------------------------------------------------------------

ALARM_TYPES = ("HI", "HIHI", "LO", "LOLO", "DEV", "ROG", "DISC")


# ---------------------------------------------------------------------------
# Alarm UDT
# ---------------------------------------------------------------------------

@dataclass
class Alarm:
    """A single alarm point per ISA-18.2 rationalization.

    Attributes:
        id:            Unique alarm identifier.
        tag_path:      Fully qualified tag path to the monitored value.
        type:          Alarm type (HI, HIHI, LO, LOLO, DEV, ROG, DISC).
        priority:      Priority level 1-4.
        state:         Current lifecycle state name.
        setpoint:      Trip setpoint value.
        deadband:      Hysteresis deadband to prevent chatter.
        delay_s:       On-delay in seconds before alarm activates.
        message:       Short alarm message shown to operator.
        consequence:   What happens if this alarm is ignored.
        response:      Documented operator response procedure.
        ts_in:         Timestamp alarm became active (epoch s).
        ts_ack:        Timestamp operator acknowledged (epoch s).
        ts_out:        Timestamp alarm returned to normal (epoch s).
        ack_user:      User ID of acknowledging operator.
        shelve_until:  Epoch seconds when shelf expires (0 = not shelved).
        shelve_reason: Reason for shelving.
    """
    id: str
    tag_path: str
    type: str = "HI"
    priority: int = 3
    state: str = "NORMAL"
    setpoint: float = 0.0
    deadband: float = 0.0
    delay_s: float = 0.0
    message: str = ""
    consequence: str = ""
    response: str = ""
    ts_in: Optional[float] = None
    ts_ack: Optional[float] = None
    ts_out: Optional[float] = None
    ack_user: Optional[str] = None
    shelve_until: float = 0.0
    shelve_reason: str = ""

    def __post_init__(self):
        if self.type not in ALARM_TYPES:
            raise ValueError(
                f"Invalid alarm type '{self.type}'; "
                f"must be one of {ALARM_TYPES}"
            )
        if not 1 <= self.priority <= 4:
            raise ValueError(f"Priority must be 1-4, got {self.priority}")

    @property
    def is_active(self) -> bool:
        return self.state in ("UNACK", "ACKED")

    @property
    def is_shelved(self) -> bool:
        return self.state == "SHELVED"

    @property
    def is_rationalized(self) -> bool:
        """True when consequence and response are documented."""
        return bool(self.consequence) and bool(self.response)

    def describe(self) -> dict:
        return {
            "id": self.id,
            "tag_path": self.tag_path,
            "type": self.type,
            "priority": self.priority,
            "state": self.state,
            "setpoint": self.setpoint,
            "message": self.message,
            "rationalized": self.is_rationalized,
        }

    def __repr__(self):
        return f"Alarm({self.id}, P{self.priority}, {self.state})"


# ---------------------------------------------------------------------------
# Alarm Class
# ---------------------------------------------------------------------------

@dataclass
class AlarmClass:
    """A classification grouping for alarms sharing common behaviour.

    Attributes:
        id:               Unique class identifier.
        name:             Human-readable class name.
        priority_default: Default priority for alarms in this class.
        sound_ref:        Reference to audible annunciation pattern.
        color_ref:        Reference to ISA-101 colour mapping.
        auto_ack:         If True, alarm auto-acknowledges on clear.
        log:              If True, all state changes are logged.
    """
    id: str
    name: str
    priority_default: int = 3
    sound_ref: str = ""
    color_ref: str = ""
    auto_ack: bool = False
    log: bool = True

    def describe(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "priority_default": self.priority_default,
            "auto_ack": self.auto_ack,
            "log": self.log,
        }

    def __repr__(self):
        return f"AlarmClass({self.id}, P{self.priority_default})"
