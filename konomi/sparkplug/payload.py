"""
Sparkplug B Payload — protobuf-modeled metric payloads.
Each payload carries a timestamp, sequence number, and a list of metrics.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from enum import IntEnum

from konomi.base import Timestamp


class SparkplugDataType(IntEnum):
    """Sparkplug B data type codes (from protobuf definition)."""
    INT8 = 1
    INT16 = 2
    INT32 = 3
    INT64 = 4
    UINT8 = 5
    UINT16 = 6
    UINT32 = 7
    UINT64 = 8
    FLOAT = 9
    DOUBLE = 10
    BOOLEAN = 11
    STRING = 12
    DATETIME = 13
    TEXT = 14
    UUID = 15
    DATASET = 16
    BYTES = 17
    FILE = 18
    TEMPLATE = 19

    @property
    def is_numeric(self) -> bool:
        return self <= SparkplugDataType.DOUBLE

    @property
    def is_integer(self) -> bool:
        return self <= SparkplugDataType.UINT64

    @property
    def byte_size(self) -> Optional[int]:
        """Fixed byte size, or None for variable-length types."""
        sizes = {1: 1, 2: 2, 3: 4, 4: 8, 5: 1, 6: 2, 7: 4, 8: 8, 9: 4, 10: 8, 11: 1}
        return sizes.get(self.value)


@dataclass
class MetricProperty:
    """A property attached to a Sparkplug metric."""
    key: str
    value: Any
    data_type: SparkplugDataType = SparkplugDataType.STRING


@dataclass
class SparkplugMetric:
    """A single metric within a Sparkplug payload."""
    name: str
    alias: Optional[int] = None
    timestamp: Optional[Timestamp] = None
    datatype: SparkplugDataType = SparkplugDataType.DOUBLE
    value: Any = None
    is_historical: bool = False
    is_transient: bool = False
    is_null: bool = False
    properties: list[MetricProperty] = field(default_factory=list)

    def add_property(self, key: str, value: Any,
                     dt: SparkplugDataType = SparkplugDataType.STRING):
        """Attach a property to this metric."""
        self.properties.append(MetricProperty(key=key, value=value, data_type=dt))

    def with_alias(self, alias: int) -> "SparkplugMetric":
        """Set the alias for bandwidth optimization. Returns self."""
        self.alias = alias
        return self

    def to_dict(self) -> dict:
        """Serialize to a dictionary."""
        d: dict[str, Any] = {"name": self.name, "datatype": self.datatype.value}
        if self.alias is not None:
            d["alias"] = self.alias
        if self.timestamp:
            d["timestamp"] = self.timestamp.epoch_ms
        if not self.is_null:
            d["value"] = self.value
        return d

    def __repr__(self):
        return f"SparkplugMetric({self.name}, {self.datatype.name}, value={self.value})"


@dataclass
class SparkplugPayload:
    """A Sparkplug B payload containing metrics and a sequence number."""
    timestamp: Timestamp = field(default_factory=Timestamp.now)
    metrics: list[SparkplugMetric] = field(default_factory=list)
    seq: int = 0
    uuid: Optional[str] = None
    body: Optional[bytes] = None

    def add_metric(self, name: str, value: Any,
                   datatype: SparkplugDataType = SparkplugDataType.DOUBLE,
                   **kwargs) -> SparkplugMetric:
        """Add a metric to this payload."""
        metric = SparkplugMetric(
            name=name, value=value, datatype=datatype, **kwargs,
        )
        self.metrics.append(metric)
        return metric

    def next_seq(self) -> int:
        """Increment sequence number with 0-255 wrap-around."""
        self.seq = (self.seq + 1) % 256
        return self.seq

    def get_metric(self, name: str) -> Optional[SparkplugMetric]:
        """Look up a metric by name."""
        for m in self.metrics:
            if m.name == name:
                return m
        return None

    @property
    def metric_count(self) -> int:
        return len(self.metrics)

    def to_dict(self) -> dict:
        """Serialize to a dictionary."""
        return {
            "timestamp": self.timestamp.epoch_ms,
            "seq": self.seq,
            "metrics": [m.to_dict() for m in self.metrics],
        }

    def __repr__(self):
        return f"SparkplugPayload(seq={self.seq}, metrics={self.metric_count})"
