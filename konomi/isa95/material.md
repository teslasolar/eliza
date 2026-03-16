# ISA-95 Material Model

Material definitions, lots, and sublots for ISA-95. `MaterialClass` defines the type of material with typed property definitions. `Material` represents a concrete material instance with lot tracking.

```python
"""
ISA-95 Material Model — material definitions, lots, and sublots.

MaterialClass defines the *type* of material (with typed property definitions).
Material represents a concrete material instance with lot tracking.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
```

## PropertyDef and MaterialClass

```python
@dataclass
class PropertyDef:
    """Definition of a material property within a MaterialClass."""
    name: str
    type: str = "str"          # str, float, int, bool
    uom: str = ""              # unit of measure
    required: bool = False

    def __repr__(self) -> str:
        req = " *" if self.required else ""
        uom = f" ({self.uom})" if self.uom else ""
        return f"PropertyDef({self.name}: {self.type}{uom}{req})"


@dataclass
class MaterialClass:
    """
    A class/type of material — defines the expected properties
    and their constraints.
    """
    id: str
    name: str
    props_def: List[PropertyDef] = field(default_factory=list)
    desc: str = ""

    def add_property(
        self,
        name: str,
        type: str = "str",
        uom: str = "",
        required: bool = False,
    ) -> "MaterialClass":
        """Add a property definition and return self for chaining."""
        self.props_def.append(
            PropertyDef(name=name, type=type, uom=uom, required=required)
        )
        return self

    def required_props(self) -> List[PropertyDef]:
        """Return only the required property definitions."""
        return [p for p in self.props_def if p.required]

    def validate(self, props: Dict[str, Any]) -> List[str]:
        """Validate a property dict against the class definitions.

        Returns a list of error strings (empty == valid).
        """
        errors: List[str] = []
        for pd in self.props_def:
            if pd.required and pd.name not in props:
                errors.append(f"Missing required property: {pd.name}")
        return errors

    def __repr__(self) -> str:
        return f"MaterialClass({self.id}, {self.name}, props={len(self.props_def)})"
```

## SubLot and Material

```python
@dataclass
class SubLot:
    """A sublot — a tracked subdivision of a lot."""
    id: str
    quantity: float = 0.0
    uom: str = ""
    props: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"SubLot({self.id}, qty={self.quantity} {self.uom})"


@dataclass
class Material:
    """A concrete material instance with lot and sublot tracking."""
    id: str
    name: str
    desc: str = ""
    material_class: Optional[str] = None
    lot: str = ""
    sublots: List[SubLot] = field(default_factory=list)
    props: Dict[str, Any] = field(default_factory=dict)

    def add_sublot(
        self,
        sublot_id: str,
        quantity: float = 0.0,
        uom: str = "",
    ) -> SubLot:
        """Create and register a sublot."""
        sl = SubLot(id=sublot_id, quantity=quantity, uom=uom)
        self.sublots.append(sl)
        return sl

    @property
    def total_quantity(self) -> float:
        """Sum of all sublot quantities."""
        return sum(s.quantity for s in self.sublots)

    def set_prop(self, key: str, value: Any) -> None:
        self.props[key] = value

    def get_prop(self, key: str, default: Any = None) -> Any:
        return self.props.get(key, default)

    def __repr__(self) -> str:
        return (
            f"Material({self.id}, {self.name}, lot={self.lot}, "
            f"sublots={len(self.sublots)})"
        )
```
