# OPC-UA Node Model

The fundamental building block of the address space. Every item in OPC-UA is a node with attributes and references.

## Enums

```python
from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum

from konomi.base import Identifier, Timestamp, Quality


class NodeClass(Enum):
    """OPC-UA node classification."""
    OBJECT = 1
    OBJECT_TYPE = 2
    VARIABLE = 3
    VARIABLE_TYPE = 4
    METHOD = 5
    VIEW = 6
    DATA_TYPE = 7
    REFERENCE_TYPE = 8


class AccessLevel(Enum):
    """Variable access level."""
    READ_ONLY = "RO"
    READ_WRITE = "RW"
    WRITE_ONLY = "WO"
```

## OPCNode

```python
@dataclass
class OPCNode:
    """A node in the OPC-UA address space."""
    node_id: str
    browse_name: str
    display_name: str
    node_class: NodeClass
    type_definition: Optional[str] = None
    parent: Optional[str] = None
    description: str = ""
    references: list = field(default_factory=list)

    @property
    def qualified_name(self) -> str:
        """Return namespace-qualified browse name."""
        return self.browse_name

    def add_reference(self, target_id: str, ref_type: str = "HasComponent"):
        """Add a reference to another node."""
        self.references.append({"target": target_id, "type": ref_type})

    def is_type(self) -> bool:
        """Check if this node defines a type."""
        return self.node_class in (
            NodeClass.OBJECT_TYPE, NodeClass.VARIABLE_TYPE,
            NodeClass.DATA_TYPE, NodeClass.REFERENCE_TYPE,
        )

    def __repr__(self):
        return f"OPCNode({self.node_id}, {self.node_class.name})"
```

## OPCVariable

```python
@dataclass
class OPCVariable(OPCNode):
    """A variable node carrying a process value with timestamps and quality."""
    data_type: str = "Double"
    value: Any = None
    source_timestamp: Optional[Timestamp] = None
    server_timestamp: Optional[Timestamp] = None
    status: Quality = field(default_factory=Quality.good)
    access_level: AccessLevel = AccessLevel.READ_ONLY
    historizing: bool = False
    array_dimensions: Optional[list] = None

    def __post_init__(self):
        if self.node_class != NodeClass.VARIABLE:
            self.node_class = NodeClass.VARIABLE

    def read(self) -> dict:
        """Read the variable value with timestamps and status."""
        return {
            "value": self.value,
            "data_type": self.data_type,
            "source_timestamp": self.source_timestamp,
            "server_timestamp": self.server_timestamp,
            "status": self.status,
        }

    def write(self, value: Any):
        """Write a new value if access permits."""
        if self.access_level == AccessLevel.READ_ONLY:
            raise PermissionError(f"Node {self.node_id} is read-only")
        self.value = value
        self.source_timestamp = Timestamp.now()
        self.server_timestamp = Timestamp.now()

    @property
    def is_writable(self) -> bool:
        return self.access_level in (AccessLevel.READ_WRITE, AccessLevel.WRITE_ONLY)

    @property
    def is_readable(self) -> bool:
        return self.access_level in (AccessLevel.READ_ONLY, AccessLevel.READ_WRITE)

    def __repr__(self):
        return (f"OPCVariable({self.node_id}, {self.data_type}, "
                f"access={self.access_level.value})")
```
