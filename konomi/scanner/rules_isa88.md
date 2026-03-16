# ISA-88 Batch Control Scan Rules

Compliance rules for ISA-88 batch control, checking for proper state machines, procedure hierarchies, and phase state tracking.

```python
"""ISA-88 Batch Control scan rules."""

import re
from konomi.meta.rules import Rule, Severity


def get_isa88_rules() -> list[Rule]:
    return [
        Rule(
            id="S88-001",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'(?:state|status)\s*[=:]\s*[\'"][a-z_]+[\'"]',
                               d.get("code", ""), re.I))
            ),
            message="Hardcoded state strings found. Use enum/constants per ISA-88 state machine.",
            severity=Severity.ERROR,
            fix="Define states as enum: class PhaseState(Enum): IDLE='idle'; RUNNING='running'",
            standard="ISA-88",
        ),
        Rule(
            id="S88-002",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'state|status|phase', d.get("code", ""), re.I)) and
                not bool(re.search(r'transition|next_state|change_state|switch.*state|if.*state',
                                   d.get("code", ""), re.I))
            ),
            message="State references found but no state machine transitions. ISA-88 requires formal state machines.",
            severity=Severity.WARN,
            fix="Implement state machine with explicit transitions, guards, and actions.",
            standard="ISA-88",
        ),
        Rule(
            id="S88-003",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'batch|recipe|procedure', d.get("code", ""), re.I)) and
                not bool(re.search(r'unit_procedure|operation.*phase|procedure.*operation',
                                   d.get("code", ""), re.I))
            ),
            message="Batch/recipe references without ISA-88 procedure hierarchy (Procedure→UnitProcedure→Operation→Phase).",
            severity=Severity.WARN,
            standard="ISA-88",
        ),
        Rule(
            id="S88-004",
            condition=lambda d: (
                d.get("type") == "factory" and
                d.get("tag_count", 0) > 0 and
                not any("Phase_State" in t for t in d.get("tags", []))
            ),
            message="Factory has no phase state tags. ISA-88 batch units need phase state tracking.",
            severity=Severity.WARN,
            standard="ISA-88",
        ),
    ]
```
