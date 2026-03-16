# OPC-UA Companion Specifications

Industry-specific information models that extend the base OPC-UA address space with domain objects.

## CompanionObject and CompanionSpec

```python
from dataclasses import dataclass, field
from typing import Optional

from konomi.meta import Entity, Relation


@dataclass
class CompanionObject:
    """An object type defined by a companion specification."""
    name: str
    type_id: str
    description: str = ""
    parent_type: Optional[str] = None
    properties: list[str] = field(default_factory=list)


@dataclass
class CompanionSpec:
    """An OPC-UA companion specification for a specific industry domain."""
    name: str
    namespace: str
    spec_url: str = ""
    version: str = "1.0"
    description: str = ""
    objects: list[CompanionObject] = field(default_factory=list)

    def add_object(self, name: str, type_id: str, **kwargs) -> CompanionObject:
        """Register an object type in this companion spec."""
        obj = CompanionObject(name=name, type_id=type_id, **kwargs)
        self.objects.append(obj)
        return obj

    def get_object(self, name: str) -> Optional[CompanionObject]:
        """Look up an object type by name."""
        for obj in self.objects:
            if obj.name == name:
                return obj
        return None

    @property
    def object_names(self) -> list[str]:
        return [o.name for o in self.objects]

    def __repr__(self):
        return f"CompanionSpec({self.name}, ns={self.namespace}, objects={len(self.objects)})"
```

## ISA-95 Companion

```python
def _build_isa95() -> CompanionSpec:
    """ISA-95 companion: Enterprise-Control System Integration."""
    spec = CompanionSpec(
        name="ISA-95",
        namespace="ns=isa95",
        version="2.0",
        description="Enterprise-Control System Integration",
    )
    for name, tid, desc in [
        ("Equipment", "isa95:EquipmentType", "Physical or logical equipment"),
        ("Material", "isa95:MaterialType", "Material definitions and lots"),
        ("Personnel", "isa95:PersonnelType", "Personnel classes and qualifications"),
        ("Process", "isa95:ProcessSegmentType", "Process segment definitions"),
    ]:
        spec.add_object(name, tid, description=desc)
    return spec
```

## PackML Companion

```python
def _build_packml() -> CompanionSpec:
    """PackML companion: Packaging Machine Language (ISA-TR88)."""
    spec = CompanionSpec(
        name="PackML",
        namespace="ns=packml",
        version="1.0",
        description="Packaging Machine Language state model",
    )
    for name, tid, desc in [
        ("StateMachine", "packml:PackMLStateMachineType", "PackML unit/machine state model"),
        ("Admin", "packml:AdminType", "Administrative commands and parameters"),
        ("Status", "packml:StatusType", "Machine status and counters"),
        ("Command", "packml:CommandType", "Machine control commands"),
    ]:
        spec.add_object(name, tid, description=desc)
    return spec
```

## MDIS Companion

```python
def _build_mdis() -> CompanionSpec:
    """MDIS companion: Subsea and Marine equipment."""
    spec = CompanionSpec(
        name="MDIS",
        namespace="ns=mdis",
        version="1.0",
        description="MDIS subsea and marine drilling equipment",
    )
    for name, tid, desc in [
        ("SubseaValve", "mdis:SubseaValveType", "Subsea valve actuator"),
        ("SubseaSensor", "mdis:SubseaSensorType", "Subsea process sensor"),
        ("SubseaChoke", "mdis:SubseaChokeType", "Subsea choke valve"),
    ]:
        spec.add_object(name, tid, description=desc)
    return spec
```

## PLCopen Companion

```python
def _build_plcopen() -> CompanionSpec:
    """PLCopen companion: Motion control and PLC programming."""
    spec = CompanionSpec(
        name="PLCopen",
        namespace="ns=plcopen",
        version="2.0",
        description="PLCopen motion control function blocks",
    )
    for name, tid, desc in [
        ("Axis", "plcopen:AxisType", "Motion control axis"),
        ("AxisGroup", "plcopen:AxisGroupType", "Coordinated axis group"),
        ("Program", "plcopen:ProgramType", "IEC 61131-3 program instance"),
        ("FunctionBlock", "plcopen:FBType", "Reusable function block"),
    ]:
        spec.add_object(name, tid, description=desc)
    return spec
```

## Pre-built Companion Instances

```python
COMPANIONS: dict[str, CompanionSpec] = {
    "ISA-95": _build_isa95(),
    "PackML": _build_packml(),
    "MDIS": _build_mdis(),
    "PLCopen": _build_plcopen(),
}
```
