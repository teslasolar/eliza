"""
OEE — Overall Equipment Effectiveness.
OEE = Availability × Performance × Quality
Target: availability>90%, performance>95%, quality>99%, oee>85%
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class OEE:
    """Overall Equipment Effectiveness calculator."""
    run_time: float = 0.0        # hours of actual production
    downtime: float = 0.0        # hours of downtime (planned + unplanned)
    actual_rate: float = 0.0     # actual units per hour
    ideal_rate: float = 1.0      # design/nameplate units per hour
    good_units: int = 0          # units passing quality check
    total_units: int = 0         # total units produced

    # Targets
    TARGET_AVAILABILITY = 0.90
    TARGET_PERFORMANCE = 0.95
    TARGET_QUALITY = 0.99
    TARGET_OEE = 0.85

    @property
    def availability(self) -> float:
        """Availability = run_time / (run_time + downtime)."""
        total = self.run_time + self.downtime
        if total == 0:
            return 0.0
        return self.run_time / total

    @property
    def performance(self) -> float:
        """Performance = actual_rate / ideal_rate."""
        if self.ideal_rate == 0:
            return 0.0
        return min(1.0, self.actual_rate / self.ideal_rate)

    @property
    def quality(self) -> float:
        """Quality = good_units / total_units."""
        if self.total_units == 0:
            return 0.0
        return self.good_units / self.total_units

    @property
    def value(self) -> float:
        """OEE = availability × performance × quality."""
        return self.availability * self.performance * self.quality

    @property
    def meets_target(self) -> bool:
        return self.value >= self.TARGET_OEE

    def gaps(self) -> dict:
        """Identify which factors are below target."""
        return {
            "availability": max(0, self.TARGET_AVAILABILITY - self.availability),
            "performance": max(0, self.TARGET_PERFORMANCE - self.performance),
            "quality": max(0, self.TARGET_QUALITY - self.quality),
        }

    def biggest_loss(self) -> str:
        """Which factor has the biggest gap to target?"""
        g = self.gaps()
        return max(g, key=g.get)

    def report(self) -> dict:
        return {
            "oee": round(self.value * 100, 1),
            "availability": round(self.availability * 100, 1),
            "performance": round(self.performance * 100, 1),
            "quality": round(self.quality * 100, 1),
            "meets_target": self.meets_target,
            "biggest_loss": self.biggest_loss(),
        }

    def __str__(self):
        return (f"OEE: {self.value*100:.1f}% "
                f"(A:{self.availability*100:.0f}% "
                f"P:{self.performance*100:.0f}% "
                f"Q:{self.quality*100:.0f}%)")
