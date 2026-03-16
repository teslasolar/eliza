# Reliability KPIs

MTBF (Mean Time Between Failures) and MTTR (Mean Time To Repair), plus downtime tracking by category.

## MTBF

```python
"""
Reliability KPIs — MTBF and MTTR.
MTBF = total_uptime / failure_count
MTTR = total_repair_time / failure_count
"""

from dataclasses import dataclass, field
from konomi.base.status import Duration, DurationUnit


@dataclass
class MTBF:
    """Mean Time Between Failures."""
    total_uptime_hours: float = 0.0
    failure_count: int = 0

    @property
    def value(self) -> float:
        """MTBF in hours."""
        if self.failure_count == 0:
            return float("inf")
        return self.total_uptime_hours / self.failure_count

    @property
    def duration(self) -> Duration:
        v = self.value if self.value != float("inf") else 0
        return Duration(value=v, unit=DurationUnit.HR)

    def record_failure(self, uptime_since_last: float):
        """Record a failure event."""
        self.total_uptime_hours += uptime_since_last
        self.failure_count += 1

    def __str__(self):
        if self.failure_count == 0:
            return "MTBF: No failures recorded"
        return f"MTBF: {self.value:.1f} hrs ({self.failure_count} failures)"
```

## MTTR

```python
@dataclass
class MTTR:
    """Mean Time To Repair."""
    total_repair_hours: float = 0.0
    repair_count: int = 0

    @property
    def value(self) -> float:
        """MTTR in hours."""
        if self.repair_count == 0:
            return 0.0
        return self.total_repair_hours / self.repair_count

    @property
    def duration(self) -> Duration:
        return Duration(value=self.value, unit=DurationUnit.HR)

    def record_repair(self, repair_duration: float):
        """Record a repair event."""
        self.total_repair_hours += repair_duration
        self.repair_count += 1

    @property
    def availability_factor(self) -> float:
        """Availability based on MTBF/MTTR (requires external MTBF)."""
        return 0.0  # needs MTBF to calculate

    def __str__(self):
        if self.repair_count == 0:
            return "MTTR: No repairs recorded"
        return f"MTTR: {self.value:.1f} hrs ({self.repair_count} repairs)"
```

## Downtime

```python
@dataclass
class Downtime:
    """Downtime tracking by category."""
    events: list = field(default_factory=list)

    CATEGORIES = ["Planned", "Unplanned", "Changeover",
                  "Setup", "Breakdown", "Idle"]

    def record(self, category: str, duration_hours: float, reason: str = ""):
        """Record a downtime event."""
        self.events.append({
            "category": category,
            "duration": duration_hours,
            "reason": reason,
        })

    def total_by_category(self) -> dict:
        """Sum hours by category."""
        totals = {c: 0.0 for c in self.CATEGORIES}
        for e in self.events:
            cat = e["category"]
            if cat in totals:
                totals[cat] += e["duration"]
        return totals

    @property
    def total_hours(self) -> float:
        return sum(e["duration"] for e in self.events)

    @property
    def unplanned_hours(self) -> float:
        return sum(e["duration"] for e in self.events
                   if e["category"] in ("Unplanned", "Breakdown"))

    def __str__(self):
        return f"Downtime: {self.total_hours:.1f} hrs ({len(self.events)} events)"
```
