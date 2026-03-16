"""
ISA-95 Personnel Model — people, roles, qualifications, and scheduling.

Personnel represents an individual worker or operator with their
qualifications and schedule reference.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Qualification:
    """A qualification or certification held by a person."""
    name: str
    level: str = ""              # e.g. "Certified", "Trainee", "Expert"
    expiry: Optional[str] = None  # ISO date string or None if no expiry
    issuer: str = ""

    @property
    def is_valid(self) -> bool:
        """True if the qualification has no expiry (non-expiring)."""
        return self.expiry is None

    def __repr__(self) -> str:
        exp = f", expires={self.expiry}" if self.expiry else ""
        return f"Qualification({self.name}, level={self.level}{exp})"


@dataclass
class Personnel:
    """A person in the ISA-95 personnel model."""
    id: str
    name: str
    role: str = ""
    qualifications: List[Qualification] = field(default_factory=list)
    schedule_ref: Optional[str] = None
    props: Dict[str, Any] = field(default_factory=dict)

    def add_qualification(
        self,
        name: str,
        level: str = "",
        expiry: Optional[str] = None,
        issuer: str = "",
    ) -> Qualification:
        """Add a qualification to this person."""
        q = Qualification(name=name, level=level, expiry=expiry, issuer=issuer)
        self.qualifications.append(q)
        return q

    def has_qualification(self, name: str) -> bool:
        """Check whether the person holds a given qualification."""
        return any(q.name == name for q in self.qualifications)

    def qualified_for(self, required: List[str]) -> bool:
        """True if the person holds *all* of the required qualifications."""
        held = {q.name for q in self.qualifications}
        return all(r in held for r in required)

    def __repr__(self) -> str:
        return (
            f"Personnel({self.id}, {self.name}, role={self.role}, "
            f"quals={len(self.qualifications)})"
        )
