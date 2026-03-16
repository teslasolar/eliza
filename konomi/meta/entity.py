"""
Entity and Relation — core objects and how they connect.
Entities reference UDTs and form hierarchies.
"""

from dataclasses import dataclass, field
from typing import Optional, Any
from enum import Enum


class RelationType(Enum):
    """How entities relate to each other."""
    CONTAINS = "contains"
    REFERENCES = "references"
    TRIGGERS = "triggers"
    PRODUCES = "produces"
    CONSUMES = "consumes"


class Cardinality(Enum):
    """Relationship cardinality."""
    ONE_TO_ONE = "1:1"
    ONE_TO_MANY = "1:N"
    MANY_TO_MANY = "N:M"


@dataclass
class Relation:
    """A relationship between two entities."""
    type: RelationType
    from_entity: str
    to_entity: str
    cardinality: Cardinality = Cardinality.ONE_TO_MANY
    desc: str = ""

    def __repr__(self):
        return (f"Relation({self.from_entity} "
                f"--{self.type.value}({self.cardinality.value})--> "
                f"{self.to_entity})")


@dataclass
class Entity:
    """A core object in a standard, typed by a UDT."""
    name: str
    udt: str                                    # references a UDT name
    parent: Optional[str] = None
    children: list = field(default_factory=list)
    tags: dict = field(default_factory=dict)     # category -> [tag definitions]
    properties: dict = field(default_factory=dict)
    _data: dict = field(default_factory=dict, repr=False)

    def add_child(self, child_name: str) -> "Entity":
        """Register a child entity name."""
        if child_name not in self.children:
            self.children.append(child_name)
        return self

    def set_tag(self, category: str, tag_name: str, value: Any):
        """Set a tag value under a category."""
        if category not in self.tags:
            self.tags[category] = {}
        self.tags[category][tag_name] = value

    def get_tag(self, category: str, tag_name: str) -> Any:
        """Get a tag value."""
        return self.tags.get(category, {}).get(tag_name)

    def set(self, key: str, value: Any):
        """Set a property."""
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a property."""
        return self._data.get(key, default)

    def path(self) -> str:
        """Get hierarchical path string."""
        parts = []
        if self.parent:
            parts.append(self.parent)
        parts.append(self.name)
        return "/".join(parts)

    def describe(self) -> dict:
        """Self-describe this entity."""
        return {
            "name": self.name,
            "udt": self.udt,
            "parent": self.parent,
            "children": self.children,
            "tag_categories": list(self.tags.keys()),
            "path": self.path(),
        }

    def __repr__(self):
        return f"Entity({self.name}, udt={self.udt}, children={len(self.children)})"
