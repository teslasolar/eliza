# ISA-95 Enterprise/Control Integration Scan Rules

Compliance rules for ISA-95 enterprise/control integration, checking for proper hierarchy, data flow through intermediate levels, and material tracking.

```python
"""ISA-95 Enterprise/Control Integration scan rules."""

import re
from konomi.meta.rules import Rule, Severity


def get_isa95_rules() -> list[Rule]:
    return [
        Rule(
            id="S95-001",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'equipment|machine|device|asset',
                               d.get("code", ""), re.I)) and
                not bool(re.search(r'site|area|work_center|work_unit|hierarchy|parent',
                                   d.get("code", ""), re.I))
            ),
            message="Equipment references without ISA-95 hierarchy (Enterprise→Site→Area→WorkCenter→WorkUnit→Equipment).",
            severity=Severity.WARN,
            standard="ISA-95",
        ),
        Rule(
            id="S95-002",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'erp|business.*plan|sap|oracle',
                               d.get("code", ""), re.I)) and
                bool(re.search(r'sensor|actuator|plc.*direct|raw.*data',
                               d.get("code", ""), re.I)) and
                not bool(re.search(r'mes|scada|gateway|middleware',
                                   d.get("code", ""), re.I))
            ),
            message="Direct L4 (business) to L0 (process) data flow. ISA-95 requires data to flow through intermediate levels.",
            severity=Severity.ERROR,
            fix="Route data through MES (L3) and SCADA (L2) layers.",
            standard="ISA-95",
        ),
        Rule(
            id="S95-003",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'material|inventory|lot|batch.*track',
                               d.get("code", ""), re.I)) and
                not bool(re.search(r'material.*class|material.*def|lot.*number|sublot',
                                   d.get("code", ""), re.I))
            ),
            message="Material tracking without ISA-95 material model (MaterialClass, Material, Lot, Sublot).",
            severity=Severity.INFO,
            standard="ISA-95",
        ),
        Rule(
            id="S95-004",
            condition=lambda d: (
                d.get("type") == "factory" and
                d.get("tag_count", 0) > 0 and
                not any("Batch_ID" in t for t in d.get("tags", []))
            ),
            message="Factory missing batch/lot tracking tags per ISA-95 material model.",
            severity=Severity.INFO,
            standard="ISA-95",
        ),
    ]
```
