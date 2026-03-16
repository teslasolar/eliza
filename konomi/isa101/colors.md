# ISA-101 Colour Semantics

Every colour maps to exactly one process meaning. All hex values target a neutral-gray (#808080) background for maximum perceptual contrast during extended operator shifts.

## ColorMeaning Dataclass

```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class ColorMeaning:
    """A single colour-to-meaning mapping per ISA-101."""
    state: str              # process state name
    hex: str                # hex colour code
    meaning: str            # what the colour communicates
    note: Optional[str] = None

    @property
    def rgb(self) -> tuple:
        """Return (R, G, B) tuple from hex."""
        h = self.hex.lstrip("#")
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    def __repr__(self):
        return f"ColorMeaning({self.state}, {self.hex})"
```

## Canonical Colour Map

```python
COLOR_MAP: list[ColorMeaning] = [
    ColorMeaning(
        state="Normal",
        hex="#808080",
        meaning="Equipment in normal idle state",
    ),
    ColorMeaning(
        state="Running",
        hex="#00AA00",
        meaning="Equipment actively running",
    ),
    ColorMeaning(
        state="Stopped",
        hex="#404040",
        meaning="Equipment stopped / de-energised",
    ),
    ColorMeaning(
        state="Warning",
        hex="#FFCC00",
        meaning="Abnormal condition, not yet alarm",
    ),
    ColorMeaning(
        state="Alarm",
        hex="#CC0000",
        meaning="Active alarm requiring operator response",
    ),
    ColorMeaning(
        state="Fault",
        hex="#CC0000",
        meaning="Equipment fault / failure",
        note="Same red as Alarm — context differentiates",
    ),
    ColorMeaning(
        state="Maintenance",
        hex="#0066CC",
        meaning="Equipment under maintenance hold",
    ),
    ColorMeaning(
        state="Disabled",
        hex="#808080",
        meaning="Equipment disabled / out of service",
        note="Gray with strikethrough or hatching overlay",
    ),
    ColorMeaning(
        state="Manual",
        hex="#FF6600",
        meaning="Equipment in manual override mode",
    ),
    ColorMeaning(
        state="Transition",
        hex="#00CCCC",
        meaning="Equipment transitioning between states",
    ),
]
```

## Lookup Helper

```python
def color_for_state(state: str) -> Optional[ColorMeaning]:
    """Look up the colour definition for a process state."""
    for cm in COLOR_MAP:
        if cm.state.upper() == state.upper():
            return cm
    return None
```
