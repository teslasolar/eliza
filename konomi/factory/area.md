# Area

A production area within a site. Contains multiple production lines. ISA-95 Area level.

```python
"""
Area — a production area within a site.
Contains multiple production lines.
ISA-95 Area level.
"""

from dataclasses import dataclass, field
from konomi.factory.line import Line
from konomi.tags.factory_tags import FactoryTagDatabase


@dataclass
class Area:
    """A production area (ISA-95 Area)."""
    name: str
    site: str = ""
    desc: str = ""
    lines: list = field(default_factory=list)
    tag_db: FactoryTagDatabase = field(default_factory=FactoryTagDatabase)

    def add_line(self, name: str, desc: str = "") -> Line:
        """Add a production line to this area."""
        line = Line(name=name, area=f"{self.site}_{self.name}", desc=desc)
        self.lines.append(line)
        self.tag_db.add_child(line.tag_db)
        return line

    def get_line(self, name: str) -> Line:
        """Get a line by name."""
        for line in self.lines:
            if line.name == name:
                return line
        return None

    @property
    def path(self) -> str:
        return f"{self.site}/{self.name}"

    @property
    def total_tags(self) -> int:
        return self.tag_db.tag_count

    def __repr__(self):
        return (f"Area({self.path}, lines={len(self.lines)}, "
                f"tags={self.total_tags})")
```
