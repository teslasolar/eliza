# MQTT Quality of Service

MQTT Quality of Service levels -- delivery guarantees for message transport. Sparkplug B relies on MQTT 3.1.1 / 5.0 as its transport layer.

```python
"""
MQTT Quality of Service levels — delivery guarantees for message transport.
Sparkplug B relies on MQTT 3.1.1 / 5.0 as its transport layer.
"""

from dataclasses import dataclass
from enum import IntEnum


class QoSLevel(IntEnum):
    """MQTT QoS levels."""
    AT_MOST_ONCE = 0
    AT_LEAST_ONCE = 1
    EXACTLY_ONCE = 2


@dataclass(frozen=True)
class MQTTQoS:
    """Detailed QoS descriptor with delivery semantics."""
    level: QoSLevel
    name: str
    delivery: str
    ack_flow: str
    use_case: str

    @property
    def guaranteed(self) -> bool:
        """Whether delivery is guaranteed at least once."""
        return self.level >= QoSLevel.AT_LEAST_ONCE

    @property
    def exactly_once(self) -> bool:
        return self.level == QoSLevel.EXACTLY_ONCE

    def __repr__(self):
        return f"MQTTQoS({self.level}, {self.name})"


# Pre-built QoS descriptors
QOS_0 = MQTTQoS(
    level=QoSLevel.AT_MOST_ONCE,
    name="AtMostOnce",
    delivery="Fire and forget",
    ack_flow="None",
    use_case="Telemetry where occasional loss is acceptable",
)

QOS_1 = MQTTQoS(
    level=QoSLevel.AT_LEAST_ONCE,
    name="AtLeastOnce",
    delivery="Guaranteed, may duplicate",
    ack_flow="PUBACK",
    use_case="State updates, alarms — must arrive at least once",
)

QOS_2 = MQTTQoS(
    level=QoSLevel.EXACTLY_ONCE,
    name="ExactlyOnce",
    delivery="Guaranteed, no duplicates",
    ack_flow="PUBREC -> PUBREL -> PUBCOMP",
    use_case="Critical commands, financial transactions",
)

QOS_LEVELS: dict[int, MQTTQoS] = {
    0: QOS_0,
    1: QOS_1,
    2: QOS_2,
}
```
