"""
Status and Duration UDTs — operational status and time durations.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class StatusSeverity(Enum):
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    FATAL = "fatal"


@dataclass
class Status:
    """An operational status with code and severity."""
    code: int
    name: str
    desc: str = ""
    severity: StatusSeverity = StatusSeverity.INFO

    @classmethod
    def ok(cls) -> "Status":
        return cls(code=0, name="OK", desc="Normal operation")

    @classmethod
    def fault(cls, desc: str = "Fault detected") -> "Status":
        return cls(code=1, name="FAULT", desc=desc, severity=StatusSeverity.ERROR)

    @classmethod
    def warning(cls, desc: str = "Warning") -> "Status":
        return cls(code=2, name="WARNING", desc=desc, severity=StatusSeverity.WARN)

    @property
    def is_ok(self) -> bool:
        return self.severity == StatusSeverity.INFO

    def __str__(self):
        return f"{self.name}({self.code}): {self.desc}"


class DurationUnit(Enum):
    MS = "ms"
    S = "s"
    MIN = "min"
    HR = "hr"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


# Conversion factors to seconds
_TO_SECONDS = {
    DurationUnit.MS: 0.001,
    DurationUnit.S: 1.0,
    DurationUnit.MIN: 60.0,
    DurationUnit.HR: 3600.0,
    DurationUnit.DAY: 86400.0,
    DurationUnit.WEEK: 604800.0,
    DurationUnit.MONTH: 2592000.0,
    DurationUnit.YEAR: 31536000.0,
}


@dataclass
class Duration:
    """A time duration with unit."""
    value: float
    unit: DurationUnit = DurationUnit.S

    @classmethod
    def seconds(cls, s: float) -> "Duration":
        return cls(value=s, unit=DurationUnit.S)

    @classmethod
    def minutes(cls, m: float) -> "Duration":
        return cls(value=m, unit=DurationUnit.MIN)

    @classmethod
    def hours(cls, h: float) -> "Duration":
        return cls(value=h, unit=DurationUnit.HR)

    @property
    def total_seconds(self) -> float:
        return self.value * _TO_SECONDS[self.unit]

    def to(self, target: DurationUnit) -> "Duration":
        """Convert to another unit."""
        secs = self.total_seconds
        return Duration(value=secs / _TO_SECONDS[target], unit=target)

    def __str__(self):
        return f"{self.value} {self.unit.value}"

    def __add__(self, other: "Duration") -> "Duration":
        return Duration.seconds(self.total_seconds + other.total_seconds)
