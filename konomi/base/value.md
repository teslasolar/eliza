# Value, Range, and Quantity

Data carriers for the system. Values carry quality and timestamp. Ranges define bounds. Quantities pair values with engineering units.

## Value

A timestamped, quality-tagged value.

```python
from dataclasses import dataclass, field
from typing import Any, Optional
from konomi.base.quality import Quality
from konomi.base.timestamp import Timestamp


@dataclass
class Value:
    """A timestamped, quality-tagged value."""
    v: Any
    q: Quality = field(default_factory=Quality.good)
    t: Timestamp = field(default_factory=Timestamp.now)
    unit: Optional[str] = None

    @classmethod
    def of(cls, v: Any, unit: str = None) -> "Value":
        """Create a good-quality value at current time."""
        return cls(v=v, unit=unit)

    @classmethod
    def bad(cls, v: Any = None) -> "Value":
        """Create a bad-quality value."""
        return cls(v=v, q=Quality.bad())

    @property
    def is_good(self) -> bool:
        return self.q.is_good

    def __str__(self):
        u = f" {self.unit}" if self.unit else ""
        return f"{self.v}{u} [{self.q.label}]"
```

## Range

A numeric range with configurable inclusive/exclusive bounds.

```python
@dataclass
class Range:
    """A numeric range with bounds."""
    lo: float
    hi: float
    lo_inclusive: bool = True
    hi_inclusive: bool = True
    unit: str = ""

    def contains(self, value: float) -> bool:
        """Check if value is within range."""
        if self.lo_inclusive:
            if value < self.lo:
                return False
        else:
            if value <= self.lo:
                return False
        if self.hi_inclusive:
            if value > self.hi:
                return False
        else:
            if value >= self.hi:
                return False
        return True

    def clamp(self, value: float) -> float:
        """Clamp value to range bounds."""
        return max(self.lo, min(self.hi, value))

    @property
    def span(self) -> float:
        return self.hi - self.lo

    def __str__(self):
        lo_br = "[" if self.lo_inclusive else "("
        hi_br = "]" if self.hi_inclusive else ")"
        return f"{lo_br}{self.lo}, {self.hi}{hi_br} {self.unit}".strip()
```

## Quantity

A value with engineering unit and optional uncertainty, supporting unit conversion.

```python
@dataclass
class Quantity:
    """A value with engineering unit and optional uncertainty."""
    value: float
    unit: str
    uncertainty: Optional[float] = None

    def convert(self, target_unit: str, factor: float) -> "Quantity":
        """Convert to another unit using a multiplication factor."""
        return Quantity(
            value=self.value * factor,
            unit=target_unit,
            uncertainty=self.uncertainty * factor if self.uncertainty else None,
        )

    def __str__(self):
        u = f" ±{self.uncertainty}" if self.uncertainty else ""
        return f"{self.value}{u} {self.unit}"
```
