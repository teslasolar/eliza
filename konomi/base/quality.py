"""
Quality UDT — OPC-UA style quality codes.
Every value in the system carries a quality indicator.
"""

from dataclasses import dataclass
from enum import IntFlag


class QualityFlags(IntFlag):
    """OPC-UA quality flags."""
    BAD = 0
    UNCERTAIN = 64
    GOOD = 192
    SUBSTITUTED = 16
    LIMITED = 4


@dataclass
class Quality:
    """Value quality with flags."""
    value: int = QualityFlags.GOOD

    @classmethod
    def good(cls) -> "Quality":
        return cls(value=QualityFlags.GOOD)

    @classmethod
    def bad(cls) -> "Quality":
        return cls(value=QualityFlags.BAD)

    @classmethod
    def uncertain(cls) -> "Quality":
        return cls(value=QualityFlags.UNCERTAIN)

    @property
    def is_good(self) -> bool:
        return (self.value & 0xC0) == QualityFlags.GOOD

    @property
    def is_bad(self) -> bool:
        return (self.value & 0xC0) == QualityFlags.BAD

    @property
    def is_uncertain(self) -> bool:
        return (self.value & 0xC0) == QualityFlags.UNCERTAIN

    @property
    def is_substituted(self) -> bool:
        return bool(self.value & QualityFlags.SUBSTITUTED)

    @property
    def is_limited(self) -> bool:
        return bool(self.value & QualityFlags.LIMITED)

    @property
    def label(self) -> str:
        if self.is_good:
            return "GOOD"
        if self.is_uncertain:
            return "UNCERTAIN"
        return "BAD"

    def __str__(self):
        return f"Quality({self.label})"
