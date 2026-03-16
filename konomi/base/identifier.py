"""
Identifier UDTs — UUID, PATH, TAG, URN.
Every entity in the system gets a unique identifier.
"""

import uuid
from dataclasses import dataclass
from typing import Optional


def make_uuid() -> str:
    """Generate a new UUID v4."""
    return str(uuid.uuid4())


@dataclass
class Identifier:
    """Base identifier with scope and format."""
    value: str
    type: str = "UUID"          # UUID, PATH, TAG, URN
    scope: str = "global"       # global, hierarchical, equipment

    @classmethod
    def uuid(cls) -> "Identifier":
        """Create a new UUID identifier."""
        return cls(value=make_uuid(), type="UUID", scope="global")

    @classmethod
    def path(cls, *parts: str) -> "Identifier":
        """Create a hierarchical path identifier: Site/Area/Line/Unit."""
        return cls(value="/".join(parts), type="PATH", scope="hierarchical")

    @classmethod
    def tag(cls, area: str, unit: str, module: str, point: str) -> "Identifier":
        """Create an equipment tag: Area_Unit_Module_Point."""
        return cls(
            value=f"{area}_{unit}_{module}_{point}",
            type="TAG", scope="equipment"
        )

    @classmethod
    def urn(cls, domain: str, type_name: str, id_value: str) -> "Identifier":
        """Create a URN: urn:domain:type:id."""
        return cls(
            value=f"urn:{domain}:{type_name}:{id_value}",
            type="URN", scope="global"
        )

    def __str__(self):
        return self.value


@dataclass
class TagPath:
    """
    Equipment tag path following ISA naming convention.
    Format: Area_Unit_Module_Point
    Example: Pkg_Filler_Tank1_Level
    """
    area: str
    unit: str
    module: str
    point: str
    desc: str = ""

    @property
    def path(self) -> str:
        return f"{self.area}_{self.unit}_{self.module}_{self.point}"

    @property
    def hierarchy(self) -> str:
        return f"{self.area}/{self.unit}/{self.module}/{self.point}"

    @classmethod
    def parse(cls, tag_str: str) -> "TagPath":
        """Parse 'Area_Unit_Module_Point' into a TagPath."""
        parts = tag_str.split("_", 3)
        if len(parts) != 4:
            raise ValueError(f"Tag must have 4 parts (Area_Unit_Module_Point): {tag_str}")
        return cls(area=parts[0], unit=parts[1], module=parts[2], point=parts[3])

    def __str__(self):
        return self.path
