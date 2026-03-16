# L5X Data Types and Tags — PLC-Side Data Definitions

This module maps konomi types to Rockwell CIP (Common Industrial Protocol) data types and generates the corresponding L5X `<DataType>` and `<Tag>` XML elements. It provides builder-style classes for constructing user-defined types (UDTs) and tag definitions, along with a mapping table that translates konomi type names to their CIP equivalents.

## CIP Types and Tag Enums

```python
"""
L5X Data Types and Tags — PLC-side data definitions.

Maps konomi types to Rockwell CIP data types and generates
L5X <DataType> and <Tag> XML elements.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum


class CIPType(Enum):
    """CIP (Common Industrial Protocol) atomic data types."""
    BOOL = "BOOL"
    SINT = "SINT"       # 8-bit signed
    INT = "INT"         # 16-bit signed
    DINT = "DINT"       # 32-bit signed
    LINT = "LINT"       # 64-bit signed
    REAL = "REAL"       # 32-bit float
    LREAL = "LREAL"     # 64-bit float
    STRING = "STRING"
    TIMER = "TIMER"
    COUNTER = "COUNTER"


class TagScope(Enum):
    """Where a tag lives in the controller."""
    CONTROLLER = "controller"
    PROGRAM = "program"
    LOCAL = "local"


class TagUsage(Enum):
    """How a tag is used."""
    NORMAL = "Normal"
    INPUT = "Input"
    OUTPUT = "Output"
    INOUT = "InOut"
```

## L5XMember and L5XDataType — User-Defined Types

```python
@dataclass
class L5XMember:
    """A member within a UDT data type."""
    name: str
    cip_type: CIPType
    dimension: int = 0       # 0 = scalar, >0 = array size
    desc: str = ""

    def to_xml(self) -> str:
        dim = f" Dimension=\"{self.dimension}\"" if self.dimension else ""
        desc_xml = ""
        if self.desc:
            desc_xml = f"\n        <Description>{self.desc}</Description>"
        return (f"      <Member Name=\"{self.name}\" "
                f"DataType=\"{self.cip_type.value}\"{dim}>"
                f"{desc_xml}\n      </Member>")


@dataclass
class L5XDataType:
    """A user-defined data type for the PLC."""
    name: str
    family: str = "NoFamily"
    members: list[L5XMember] = field(default_factory=list)
    desc: str = ""

    def add_member(self, name: str, cip_type: CIPType, **kw) -> "L5XDataType":
        self.members.append(L5XMember(name=name, cip_type=cip_type, **kw))
        return self

    def add_bool(self, name: str, desc: str = "") -> "L5XDataType":
        return self.add_member(name, CIPType.BOOL, desc=desc)

    def add_dint(self, name: str, desc: str = "") -> "L5XDataType":
        return self.add_member(name, CIPType.DINT, desc=desc)

    def add_real(self, name: str, desc: str = "") -> "L5XDataType":
        return self.add_member(name, CIPType.REAL, desc=desc)

    def add_string(self, name: str, desc: str = "") -> "L5XDataType":
        return self.add_member(name, CIPType.STRING, desc=desc)

    def add_timer(self, name: str, desc: str = "") -> "L5XDataType":
        return self.add_member(name, CIPType.TIMER, desc=desc)

    def to_xml(self) -> str:
        members_xml = "\n".join(m.to_xml() for m in self.members)
        return (f"  <DataType Name=\"{self.name}\" "
                f"Family=\"{self.family}\">\n"
                f"    <Description>{self.desc}</Description>\n"
                f"    <Members>\n{members_xml}\n"
                f"    </Members>\n"
                f"  </DataType>")

    def __repr__(self):
        return f"L5XDataType({self.name}, members={len(self.members)})"
```

## L5XTag — PLC Tag Definitions

```python
@dataclass
class L5XTag:
    """A PLC tag definition."""
    name: str
    data_type: str              # CIP type name or UDT name
    scope: TagScope = TagScope.CONTROLLER
    usage: TagUsage = TagUsage.NORMAL
    value: Any = None
    desc: str = ""
    dimension: int = 0
    constant: bool = False
    external_access: str = "Read/Write"

    def to_xml(self) -> str:
        dim = f" Dimensions=\"{self.dimension}\"" if self.dimension else ""
        const = " Constant=\"true\"" if self.constant else ""
        val = ""
        if self.value is not None:
            val = f"\n    <Data Format=\"Decorated\"><DataValue Value=\"{self.value}\"/></Data>"
        desc_xml = ""
        if self.desc:
            desc_xml = f"\n    <Description>{self.desc}</Description>"
        return (f"  <Tag Name=\"{self.name}\" TagType=\"Base\" "
                f"DataType=\"{self.data_type}\" "
                f"Usage=\"{self.usage.value}\" "
                f"ExternalAccess=\"{self.external_access}\""
                f"{dim}{const}>{desc_xml}{val}\n  </Tag>")

    def __repr__(self):
        return f"L5XTag({self.name}: {self.data_type})"
```

## Konomi-to-CIP Type Mapping

```python
# ── konomi-to-CIP type mapping ──────────────────────────────────────

KONOMI_TO_CIP = {
    "analog":   CIPType.REAL,
    "discrete": CIPType.BOOL,
    "string":   CIPType.STRING,
    "integer":  CIPType.DINT,
    "enum":     CIPType.DINT,
    "float":    CIPType.REAL,
    "bool":     CIPType.BOOL,
    "int":      CIPType.DINT,
    "str":      CIPType.STRING,
}


def konomi_to_cip(type_name: str) -> CIPType:
    """Map a konomi type name to a CIP type."""
    return KONOMI_TO_CIP.get(type_name.lower(), CIPType.DINT)
```
