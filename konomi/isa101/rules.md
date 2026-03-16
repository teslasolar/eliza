# ISA-101 Rules

Enforceable constraints for HMI design compliance. Each rule is an instance of `konomi.meta.rules.Rule` so it can be loaded into a RuleEngine alongside rules from other standards.

## Rule Definitions

```python
from konomi.meta.rules import Rule, Severity

_STD = "ISA-101"

R1 = Rule(
    id="ISA101-R1",
    condition=lambda d: d.get("hardcoded_values", False),
    message="No hard-coded values in graphics — all data must come from tags.",
    severity=Severity.ERROR,
    fix="Replace literal values with tag bindings.",
    standard=_STD,
)

R2 = Rule(
    id="ISA101-R2",
    condition=lambda d: d.get("direct_address", False),
    message="Bind to tag path, not direct PLC address.",
    severity=Severity.ERROR,
    fix="Use symbolic tag path (e.g. Area_Unit_Module_Point) instead of "
        "direct address (e.g. %MW100).",
    standard=_STD,
)

R3 = Rule(
    id="ISA101-R3",
    condition=lambda d: not d.get("uses_template", True),
    message="Graphic instances must inherit from a template.",
    severity=Severity.WARN,
    fix="Create a master template and derive instances via inheritance.",
    standard=_STD,
)

R4 = Rule(
    id="ISA101-R4",
    condition=lambda d: not d.get("centralized_styles", True),
    message="Style definitions must be centralized, not per-element.",
    severity=Severity.WARN,
    fix="Move colours, fonts, and line widths to a shared style sheet.",
    standard=_STD,
)

R5 = Rule(
    id="ISA101-R5",
    condition=lambda d: not d.get("alarm_visible_all_layers", True),
    message="Alarm indication must be visible at all display layers.",
    severity=Severity.ERROR,
    fix="Propagate alarm colour/badge from L3 up to L1 overview.",
    standard=_STD,
)

R6 = Rule(
    id="ISA101-R6",
    condition=lambda d: not d.get("consistent_navigation", True),
    message="Navigation must be consistent and predictable across displays.",
    severity=Severity.WARN,
    fix="Use a fixed nav bar or breadcrumb at the same screen position.",
    standard=_STD,
)

R7 = Rule(
    id="ISA101-R7",
    condition=lambda d: not d.get("controls_labeled", True),
    message="All controls must be labeled with engineering units shown.",
    severity=Severity.WARN,
    fix="Add label and unit annotation to every operator input.",
    standard=_STD,
)

R8 = Rule(
    id="ISA101-R8",
    condition=lambda d: (
        d.get("critical_command", False)
        and not d.get("confirmation_required", False)
    ),
    message="Critical commands require operator confirmation dialog.",
    severity=Severity.ERROR,
    fix="Add a confirm/cancel dialog before executing the command.",
    standard=_STD,
)
```

## Collected List for Bulk Registration

```python
ISA101_RULES: list[Rule] = [R1, R2, R3, R4, R5, R6, R7, R8]
```
