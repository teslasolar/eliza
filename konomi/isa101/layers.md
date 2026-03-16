# ISA-101 Display Layers

Five levels of progressive detail for HMI display hierarchy.

| Level | Name     | Scope       |
|-------|----------|-------------|
| L1    | Overview | Plant/Site  |
| L2    | Area     | Process Area|
| L3    | Unit     | Equipment   |
| L4    | Detail   | Diagnostic  |
| L5    | Support  | Maintenance |

## HMILayer Dataclass

```python
from dataclasses import dataclass, field
from typing import List


@dataclass
class HMILayer:
    """One layer in the ISA-101 five-layer display hierarchy."""
    level: int                       # 1-5
    name: str                        # short name (Overview, Area, …)
    scope: str                       # what this layer covers
    content: str                     # what the operator sees
    nav_to: List[int] = field(default_factory=list)  # layers reachable

    @property
    def label(self) -> str:
        return f"L{self.level}: {self.name}"

    def describe(self) -> dict:
        return {
            "level": self.level,
            "name": self.name,
            "scope": self.scope,
            "content": self.content,
            "nav_to": [f"L{n}" for n in self.nav_to],
        }

    def __repr__(self):
        return f"HMILayer(L{self.level} {self.name})"
```

## Canonical Layer Definitions

```python
LAYERS: List[HMILayer] = [
    HMILayer(
        level=1,
        name="Overview",
        scope="Plant / Site",
        content="KPIs, overall status, active alarms, production totals",
        nav_to=[2],
    ),
    HMILayer(
        level=2,
        name="Area",
        scope="Process Area",
        content="Process flows, equipment states, area trends",
        nav_to=[1, 3],
    ),
    HMILayer(
        level=3,
        name="Unit",
        scope="Equipment",
        content="Faceplates, control loops, direct commands",
        nav_to=[2, 4],
    ),
    HMILayer(
        level=4,
        name="Detail",
        scope="Diagnostic",
        content="Configuration parameters, tuning constants, IO detail",
        nav_to=[3, 5],
    ),
    HMILayer(
        level=5,
        name="Support",
        scope="Maintenance",
        content="Calibration records, maintenance history, spare parts",
        nav_to=[4],
    ),
]
```

## Lookup Helper

```python
def get_layer(level: int) -> HMILayer:
    """Look up a layer by its level number (1-5)."""
    for layer in LAYERS:
        if layer.level == level:
            return layer
    raise ValueError(f"No layer with level {level}; valid range is 1-5")
```
