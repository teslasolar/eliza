# Timestamp

Timestamp UDT supporting ISO8601, epoch milliseconds, and OPC FileTime formats. All time in the system flows through this type.

```python
from dataclasses import dataclass
from datetime import datetime, timezone
import time


@dataclass
class Timestamp:
    """A timestamp with multiple format support."""
    value: float                  # epoch seconds (float for ms precision)
    format: str = "ISO8601"       # ISO8601, EPOCH_MS, OPC_FILETIME

    @classmethod
    def now(cls) -> "Timestamp":
        """Create a timestamp for right now."""
        return cls(value=time.time())

    @classmethod
    def from_iso(cls, iso_str: str) -> "Timestamp":
        """Parse an ISO8601 string."""
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return cls(value=dt.timestamp(), format="ISO8601")

    @classmethod
    def from_epoch_ms(cls, ms: int) -> "Timestamp":
        """Create from epoch milliseconds."""
        return cls(value=ms / 1000.0, format="EPOCH_MS")

    @property
    def iso8601(self) -> str:
        """Format as ISO8601 UTC string."""
        dt = datetime.fromtimestamp(self.value, tz=timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{int(dt.microsecond/1000):03d}Z"

    @property
    def epoch_ms(self) -> int:
        """Format as epoch milliseconds."""
        return int(self.value * 1000)

    @property
    def datetime(self) -> datetime:
        """Convert to Python datetime (UTC)."""
        return datetime.fromtimestamp(self.value, tz=timezone.utc)

    def elapsed_since(self, other: "Timestamp") -> float:
        """Seconds elapsed since another timestamp."""
        return self.value - other.value

    def __str__(self):
        return self.iso8601

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value
```
