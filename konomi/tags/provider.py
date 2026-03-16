"""
Tag Provider — base class for all tag sources.
Tags are the fundamental data points in industrial automation.
Every sensor, actuator, setpoint, and status is a tag.
"""

from dataclasses import dataclass, field
from typing import Any, Optional, Callable
from enum import Enum
from konomi.base.quality import Quality
from konomi.base.timestamp import Timestamp
from konomi.base.value import Value


class TagType(Enum):
    """Tag data types."""
    ANALOG = "analog"       # continuous value (float)
    DISCRETE = "discrete"   # binary (bool)
    STRING = "string"       # text
    INTEGER = "integer"     # integer
    ENUM = "enum"           # enumerated value


@dataclass
class Tag:
    """A single data point in the system."""
    path: str                          # Area_Unit_Module_Point
    type: TagType = TagType.ANALOG
    desc: str = ""
    unit: str = ""
    range_lo: Optional[float] = None
    range_hi: Optional[float] = None
    _value: Any = field(default=None, repr=False)
    _quality: Quality = field(default_factory=Quality.good, repr=False)
    _timestamp: Timestamp = field(default_factory=Timestamp.now, repr=False)
    _sim_fn: Optional[Callable] = field(default=None, repr=False)

    def read(self) -> Value:
        """Read current tag value."""
        if self._sim_fn is not None:
            self._value = self._sim_fn()
            self._timestamp = Timestamp.now()
        return Value(v=self._value, q=self._quality,
                     t=self._timestamp, unit=self.unit)

    def write(self, value: Any):
        """Write a value to this tag."""
        self._value = value
        self._timestamp = Timestamp.now()
        self._quality = Quality.good()

    def set_sim(self, fn: Callable):
        """Set a simulation function for this tag."""
        self._sim_fn = fn

    def set_bad(self):
        """Mark tag quality as bad."""
        self._quality = Quality.bad()

    @property
    def value(self) -> Any:
        return self._value

    def __str__(self):
        v = self.read()
        return f"{self.path}: {v}"


class TagProvider:
    """Base class for tag collections."""

    def __init__(self, prefix: str = ""):
        self.prefix = prefix
        self._tags: dict[str, Tag] = {}

    def register(self, tag: Tag) -> Tag:
        """Register a tag."""
        full_path = f"{self.prefix}_{tag.path}" if self.prefix else tag.path
        tag.path = full_path
        self._tags[full_path] = tag
        return tag

    def get(self, path: str) -> Optional[Tag]:
        """Get a tag by path."""
        return self._tags.get(path)

    def read_all(self) -> dict[str, Value]:
        """Read all tags."""
        return {path: tag.read() for path, tag in self._tags.items()}

    def paths(self) -> list[str]:
        """Get all tag paths."""
        return list(self._tags.keys())

    @property
    def count(self) -> int:
        return len(self._tags)

    def __iter__(self):
        return iter(self._tags.values())

    def __repr__(self):
        return f"TagProvider({self.prefix}, tags={self.count})"
