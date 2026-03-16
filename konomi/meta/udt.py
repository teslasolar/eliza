"""
User Defined Types — the building blocks of all standards.
Every piece of data in the system is typed via UDTs.
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Field:
    """A field within a UDT."""
    name: str
    type: str                          # python type name or UDT reference
    unit: Optional[str] = None         # engineering unit (PSI, degC, etc.)
    range_lo: Optional[float] = None   # valid range lower bound
    range_hi: Optional[float] = None   # valid range upper bound
    desc: str = ""
    required: bool = True
    default: Any = None

    def validate(self, value) -> Optional[str]:
        """Validate a value against this field definition."""
        if value is None and self.required:
            return f"{self.name}: required field is None"
        if value is None:
            return None
        if self.range_lo is not None and value < self.range_lo:
            return f"{self.name}: {value} below minimum {self.range_lo}"
        if self.range_hi is not None and value > self.range_hi:
            return f"{self.name}: {value} above maximum {self.range_hi}"
        return None


@dataclass
class UDT:
    """User Defined Type — a structured data template."""
    name: str
    base: Optional[str] = None         # inherits from another UDT
    fields: list = field(default_factory=list)
    methods: list = field(default_factory=list)
    constraints: list = field(default_factory=list)
    desc: str = ""

    def add_field(self, name: str, type: str, **kwargs) -> "UDT":
        """Add a field to this UDT. Returns self for chaining."""
        self.fields.append(Field(name=name, type=type, **kwargs))
        return self

    def get_field(self, name: str) -> Optional[Field]:
        """Look up a field by name."""
        for f in self.fields:
            if f.name == name:
                return f
        return None

    def validate(self, data: dict) -> list:
        """Validate a dict of data against this UDT's fields."""
        errors = []
        for f in self.fields:
            value = data.get(f.name)
            err = f.validate(value)
            if err:
                errors.append(err)
        return errors

    def instantiate(self, **kwargs) -> dict:
        """Create an instance with defaults filled in."""
        instance = {}
        for f in self.fields:
            if f.name in kwargs:
                instance[f.name] = kwargs[f.name]
            elif f.default is not None:
                instance[f.name] = f.default
            else:
                instance[f.name] = None
        return instance

    def field_names(self) -> list:
        """Return list of field names."""
        return [f.name for f in self.fields]

    def __repr__(self):
        return f"UDT({self.name}, fields={len(self.fields)})"
