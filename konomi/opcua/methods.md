# OPC-UA Methods and Subscriptions

Callable endpoints and data change monitoring via the publish/subscribe model.

## MethodArg and OPCMethod

```python
from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum

from konomi.base import Identifier


@dataclass
class MethodArg:
    """An argument to an OPC-UA method (input or output)."""
    name: str
    data_type: str
    description: str = ""
    value_rank: int = -1  # -1=scalar, 0=array, 1=1D, 2=2D


@dataclass
class OPCMethod:
    """A callable method node in the OPC-UA address space."""
    node_id: str
    browse_name: str
    display_name: str
    parent: Optional[str] = None
    input_args: list[MethodArg] = field(default_factory=list)
    output_args: list[MethodArg] = field(default_factory=list)
    executable: bool = True
    user_executable: bool = True
    description: str = ""

    def add_input(self, name: str, data_type: str, **kwargs) -> "OPCMethod":
        """Add an input argument. Returns self for chaining."""
        self.input_args.append(MethodArg(name=name, data_type=data_type, **kwargs))
        return self

    def add_output(self, name: str, data_type: str, **kwargs) -> "OPCMethod":
        """Add an output argument. Returns self for chaining."""
        self.output_args.append(MethodArg(name=name, data_type=data_type, **kwargs))
        return self

    @property
    def signature(self) -> str:
        """Human-readable method signature."""
        inputs = ", ".join(f"{a.name}:{a.data_type}" for a in self.input_args)
        outputs = ", ".join(f"{a.name}:{a.data_type}" for a in self.output_args)
        return f"{self.browse_name}({inputs}) -> ({outputs})"

    def __repr__(self):
        return (f"OPCMethod({self.browse_name}, "
                f"in={len(self.input_args)}, out={len(self.output_args)})")
```

## FilterType and MonitoredItem

```python
class FilterType(Enum):
    """Monitored item filter types."""
    DATA_CHANGE = "data_change"
    EVENT = "event"
    AGGREGATE = "aggregate"


@dataclass
class MonitoredItem:
    """A monitored item within a subscription."""
    item_id: int
    node_id: str
    sampling_interval: float = 1000.0  # ms
    queue_size: int = 1
    discard_oldest: bool = True
    filter_type: FilterType = FilterType.DATA_CHANGE
    deadband_value: float = 0.0

    def __repr__(self):
        return (f"MonitoredItem({self.item_id}, node={self.node_id}, "
                f"sample={self.sampling_interval}ms)")
```

## Subscription

```python
@dataclass
class Subscription:
    """An OPC-UA subscription for data change notifications."""
    subscription_id: int
    publishing_interval: float = 1000.0  # ms
    lifetime_count: int = 300
    max_keepalive_count: int = 10
    priority: int = 0
    enabled: bool = True
    monitored_items: list[MonitoredItem] = field(default_factory=list)

    def add_item(self, node_id: str, **kwargs) -> MonitoredItem:
        """Add a monitored item to this subscription."""
        item_id = len(self.monitored_items) + 1
        item = MonitoredItem(item_id=item_id, node_id=node_id, **kwargs)
        self.monitored_items.append(item)
        return item

    def remove_item(self, item_id: int) -> bool:
        """Remove a monitored item by ID."""
        for i, item in enumerate(self.monitored_items):
            if item.item_id == item_id:
                self.monitored_items.pop(i)
                return True
        return False

    @property
    def item_count(self) -> int:
        return len(self.monitored_items)

    def __repr__(self):
        return (f"Subscription({self.subscription_id}, "
                f"interval={self.publishing_interval}ms, "
                f"items={self.item_count})")
```
