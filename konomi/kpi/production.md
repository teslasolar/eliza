# Production KPIs

CycleTime, Throughput, and FirstPassYield measurements for production performance tracking.

## CycleTime

```python
"""
Production KPIs — CycleTime, Throughput, FirstPassYield.
"""

from dataclasses import dataclass
from konomi.base.status import Duration, DurationUnit


@dataclass
class CycleTime:
    """Cycle time measurement vs. ideal."""
    ideal_seconds: float = 0.0
    actual_seconds: float = 0.0

    @property
    def efficiency(self) -> float:
        """Cycle time efficiency = ideal / actual."""
        if self.actual_seconds == 0:
            return 0.0
        return min(1.0, self.ideal_seconds / self.actual_seconds)

    @property
    def loss_seconds(self) -> float:
        """Time lost per cycle vs. ideal."""
        return max(0, self.actual_seconds - self.ideal_seconds)

    def record(self, actual: float):
        """Record an actual cycle time."""
        self.actual_seconds = actual

    def __str__(self):
        return (f"CycleTime: {self.actual_seconds:.1f}s "
                f"(ideal {self.ideal_seconds:.1f}s, "
                f"eff {self.efficiency*100:.0f}%)")
```

## Throughput

```python
@dataclass
class Throughput:
    """Throughput measurement."""
    units_produced: int = 0
    period_hours: float = 1.0

    @property
    def rate(self) -> float:
        """Units per hour."""
        if self.period_hours == 0:
            return 0.0
        return self.units_produced / self.period_hours

    def record_production(self, units: int, hours: float):
        """Record a production period."""
        self.units_produced += units
        self.period_hours += hours

    def __str__(self):
        return f"Throughput: {self.rate:.1f} units/hr"
```

## FirstPassYield

```python
@dataclass
class FirstPassYield:
    """First Pass Yield — good on first attempt."""
    good_first_time: int = 0
    total_attempted: int = 0

    @property
    def value(self) -> float:
        """FPY percentage."""
        if self.total_attempted == 0:
            return 0.0
        return self.good_first_time / self.total_attempted

    def record(self, good: bool):
        """Record a unit attempt."""
        self.total_attempted += 1
        if good:
            self.good_first_time += 1

    @property
    def rework_rate(self) -> float:
        """Percentage requiring rework."""
        return 1.0 - self.value

    def __str__(self):
        return f"FPY: {self.value*100:.1f}% ({self.good_first_time}/{self.total_attempted})"
```
