# L5X Program and Task — PLC Program Structure

This module defines the top-level organizational containers for PLC logic. An `L5XProgram` holds routines (ladder logic) and program-scoped tags, while an `L5XTask` schedules one or more programs with a configurable scan rate, priority, and watchdog timer. Together they model the program/task hierarchy that Rockwell Studio 5000 expects.

## TaskType Enum and L5XProgram

```python
"""
L5X Program and Task — PLC program structure.

A Program contains routines (ladder logic) and program-scoped tags.
A Task schedules one or more programs with a scan rate.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from konomi.l5x.rungs import LadderRoutine
from konomi.l5x.datatypes import L5XTag


class TaskType(Enum):
    """PLC task types."""
    CONTINUOUS = "CONTINUOUS"
    PERIODIC = "PERIODIC"
    EVENT = "EVENT"


@dataclass
class L5XProgram:
    """A PLC program containing routines and tags."""
    name: str
    desc: str = ""
    main_routine: str = "MainRoutine"
    routines: list[LadderRoutine] = field(default_factory=list)
    tags: list[L5XTag] = field(default_factory=list)
    disabled: bool = False

    def add_routine(self, name: str, desc: str = "") -> LadderRoutine:
        """Create and add a routine."""
        r = LadderRoutine(name=name, desc=desc)
        self.routines.append(r)
        return r

    def add_tag(self, name: str, data_type: str, **kw) -> L5XTag:
        """Create and add a program-scoped tag."""
        from konomi.l5x.datatypes import TagScope
        tag = L5XTag(name=name, data_type=data_type,
                     scope=TagScope.PROGRAM, **kw)
        self.tags.append(tag)
        return tag

    def validate(self) -> list[str]:
        errors = []
        if not self.routines:
            errors.append(f"Program {self.name}: no routines defined")
        main_names = [r.name for r in self.routines]
        if self.main_routine not in main_names and self.routines:
            errors.append(f"Program {self.name}: main routine "
                          f"'{self.main_routine}' not found")
        for r in self.routines:
            errors.extend(r.validate())
        return errors

    def to_xml(self) -> str:
        tags_xml = "\n".join(t.to_xml() for t in self.tags)
        routines_xml = "\n".join(r.to_xml() for r in self.routines)
        disabled = " Disabled=\"true\"" if self.disabled else ""
        return (f"<Program Name=\"{self.name}\" "
                f"MainRoutineName=\"{self.main_routine}\""
                f"{disabled}>\n"
                f"  <Description>{self.desc}</Description>\n"
                f"  <Tags>\n{tags_xml}\n  </Tags>\n"
                f"  <Routines>\n{routines_xml}\n  </Routines>\n"
                f"</Program>")

    def __repr__(self):
        return (f"L5XProgram({self.name}, routines="
                f"{len(self.routines)}, tags={len(self.tags)})")
```

## L5XTask — Scheduling Programs on the PLC

```python
@dataclass
class L5XTask:
    """A PLC task that schedules programs."""
    name: str
    task_type: TaskType = TaskType.CONTINUOUS
    rate: float = 10.0          # ms for periodic tasks
    priority: int = 10          # 1 (highest) to 15 (lowest)
    watchdog: float = 500.0     # ms
    programs: list[str] = field(default_factory=list)
    desc: str = ""

    def to_xml(self) -> str:
        progs = "\n".join(
            f"    <ScheduledProgram Name=\"{p}\"/>"
            for p in self.programs
        )
        return (f"  <Task Name=\"{self.name}\" "
                f"Type=\"{self.task_type.value}\" "
                f"Rate=\"{self.rate}\" "
                f"Priority=\"{self.priority}\" "
                f"Watchdog=\"{self.watchdog}\">\n"
                f"    <Description>{self.desc}</Description>\n"
                f"{progs}\n"
                f"  </Task>")

    def __repr__(self):
        return (f"L5XTask({self.name}, {self.task_type.value}, "
                f"programs={len(self.programs)})")
```
