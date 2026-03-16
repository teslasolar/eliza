"""
ISA-18.2 Alarm Priorities — four levels from Emergency to Low.

Each priority defines response urgency, maximum response time, colour,
and audible annunciation pattern.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AlarmPriority:
    """A single alarm priority level per ISA-18.2."""
    level: int                  # 1-4
    name: str                   # Emergency, High, Medium, Low
    response: str               # Immediate, Prompt, Timely, Awareness
    max_response_time: str      # human-readable (<1min, <10min, …)
    max_response_s: float       # seconds
    color: str                  # hex colour
    sound: str                  # annunciation pattern

    @property
    def label(self) -> str:
        return f"P{self.level}: {self.name}"

    def describe(self) -> dict:
        return {
            "level": self.level,
            "name": self.name,
            "response": self.response,
            "max_response_time": self.max_response_time,
            "color": self.color,
            "sound": self.sound,
        }

    def __repr__(self):
        return f"AlarmPriority(P{self.level} {self.name})"


# ---------------------------------------------------------------------------
# Canonical priority definitions
# ---------------------------------------------------------------------------

PRIORITIES: list[AlarmPriority] = [
    AlarmPriority(
        level=1,
        name="Emergency",
        response="Immediate",
        max_response_time="<1 min",
        max_response_s=60.0,
        color="#CC0000",
        sound="Continuous",
    ),
    AlarmPriority(
        level=2,
        name="High",
        response="Prompt",
        max_response_time="<10 min",
        max_response_s=600.0,
        color="#FF6600",
        sound="Fast pulse",
    ),
    AlarmPriority(
        level=3,
        name="Medium",
        response="Timely",
        max_response_time="<1 hr",
        max_response_s=3600.0,
        color="#FFCC00",
        sound="Slow pulse",
    ),
    AlarmPriority(
        level=4,
        name="Low",
        response="Awareness",
        max_response_time="Within shift",
        max_response_s=43200.0,
        color="#00CCCC",
        sound="None",
    ),
]


def get_priority(level: int) -> AlarmPriority:
    """Look up a priority by its level number (1-4)."""
    for p in PRIORITIES:
        if p.level == level:
            return p
    raise ValueError(f"No priority with level {level}; valid range is 1-4")
