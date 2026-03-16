# ISA-101 Graphic Elements

Reusable display objects, faceplates, and trends. Elements bind to tag paths (never hard-coded addresses) and inherit appearance from centralised style definitions.

## GraphicElement

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class GraphicElement:
    """A single graphic object on an HMI display.

    Attributes:
        id: Unique element identifier.
        type: Equipment type drawn (Tank, Valve, Pump, etc.).
        tags: Tag bindings keyed by role (pv, sp, cmd, sts, mode).
        states: Possible visual states this element can show.
        appearance: Style references (template, fill rule, colours).
    """
    id: str
    type: str                                   # Tank|Valve|Pump|Motor|Conveyor|Pipe|Sensor
    tags: Dict[str, str] = field(default_factory=dict)
    states: List[str] = field(default_factory=list)
    appearance: Dict[str, str] = field(default_factory=dict)

    VALID_TYPES = (
        "Tank", "Valve", "Pump", "Motor",
        "Conveyor", "Pipe", "Sensor",
    )

    TAG_ROLES = ("pv", "sp", "cmd", "sts", "mode")

    def bind_tag(self, role: str, tag_path: str) -> "GraphicElement":
        """Bind a tag path to a role. Returns self for chaining."""
        if role not in self.TAG_ROLES:
            raise ValueError(f"Invalid role '{role}'; use one of {self.TAG_ROLES}")
        self.tags[role] = tag_path
        return self

    def set_style(self, key: str, value: str) -> "GraphicElement":
        """Set an appearance property. Returns self for chaining."""
        self.appearance[key] = value
        return self

    def describe(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "tags": dict(self.tags),
            "states": list(self.states),
        }

    def __repr__(self):
        return f"GraphicElement({self.id}, {self.type})"
```

## Faceplate

```python
@dataclass
class Faceplate:
    """An interactive control panel for a single piece of equipment.

    Faceplates appear at L3 (Unit) and are reachable from L2 / L4.
    """
    equipment_ref: str              # GraphicElement.id or tag path root
    title: str
    pv_display: str                 # tag path for process value
    sp_input: Optional[str] = None  # tag path for setpoint entry
    commands: List[str] = field(default_factory=list)   # Start, Stop, Reset …
    status_tags: Dict[str, str] = field(default_factory=dict)
    nav: Dict[str, int] = field(default_factory=dict)   # label -> layer level

    def add_command(self, cmd: str) -> "Faceplate":
        """Register an operator command."""
        self.commands.append(cmd)
        return self

    def add_status(self, label: str, tag_path: str) -> "Faceplate":
        """Add a status indicator."""
        self.status_tags[label] = tag_path
        return self

    def describe(self) -> dict:
        return {
            "equipment": self.equipment_ref,
            "title": self.title,
            "pv": self.pv_display,
            "sp": self.sp_input,
            "commands": self.commands,
            "status": dict(self.status_tags),
            "nav": dict(self.nav),
        }

    def __repr__(self):
        return f"Faceplate({self.title})"
```

## TrendPen and Trend

```python
@dataclass
class TrendPen:
    """A single pen (trace) on a trend display."""
    tag_path: str
    color: str = "#FFFFFF"
    scale_lo: float = 0.0
    scale_hi: float = 100.0
    unit: str = ""


@dataclass
class Trend:
    """A real-time / historical trend chart.

    Attributes:
        pens: Tag traces to plot.
        timespan_s: Visible time window in seconds.
        sample_rate_s: Data sample interval in seconds.
    """
    pens: List[TrendPen] = field(default_factory=list)
    timespan_s: float = 3600.0      # default 1 hour
    sample_rate_s: float = 1.0      # default 1 second

    def add_pen(self, tag_path: str, **kwargs) -> "Trend":
        """Add a pen to this trend. Returns self for chaining."""
        self.pens.append(TrendPen(tag_path=tag_path, **kwargs))
        return self

    def describe(self) -> dict:
        return {
            "pen_count": len(self.pens),
            "timespan_s": self.timespan_s,
            "sample_rate_s": self.sample_rate_s,
            "tags": [p.tag_path for p in self.pens],
        }

    def __repr__(self):
        return f"Trend(pens={len(self.pens)}, span={self.timespan_s}s)"
```
