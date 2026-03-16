"""
ISA-18.2 Rules — rationalization and management constraints.

Each rule is an instance of konomi.meta.rules.Rule so it can be loaded
into a RuleEngine alongside rules from other standards.
"""

from konomi.meta.rules import Rule, Severity

_STD = "ISA-18.2"

# ---------------------------------------------------------------------------
# Rule definitions
# ---------------------------------------------------------------------------

R1 = Rule(
    id="ISA18-R1",
    condition=lambda d: not d.get("documented", True),
    message="Every alarm must be documented in the alarm database.",
    severity=Severity.ERROR,
    fix="Complete the alarm rationalization record with consequence, "
        "response, and classification.",
    standard=_STD,
)

R2 = Rule(
    id="ISA18-R2",
    condition=lambda d: not d.get("unique_response", True),
    message="Every alarm must have a unique, specific operator response.",
    severity=Severity.ERROR,
    fix="Write a distinct response procedure; avoid generic 'investigate' "
        "instructions.",
    standard=_STD,
)

R3 = Rule(
    id="ISA18-R3",
    condition=lambda d: not d.get("actionable", True),
    message="Every alarm must be actionable — operator can do something.",
    severity=Severity.ERROR,
    fix="If no operator action exists, reclassify as event/alert or remove.",
    standard=_STD,
)

R4 = Rule(
    id="ISA18-R4",
    condition=lambda d: d.get("priority_arbitrary", False),
    message="Priority must be based on consequence severity and required "
            "response time, not arbitrary assignment.",
    severity=Severity.WARN,
    fix="Use a consequence / response-time matrix to assign priority.",
    standard=_STD,
)

R5 = Rule(
    id="ISA18-R5",
    condition=lambda d: d.get("duplicate_alarm", False),
    message="No duplicate alarms for the same process condition.",
    severity=Severity.WARN,
    fix="Consolidate duplicates into a single alarm with clear ownership.",
    standard=_STD,
)

R6 = Rule(
    id="ISA18-R6",
    condition=lambda d: d.get("review_gap_days", 0) > 365,
    message="Alarm rationalization review must occur at least annually.",
    severity=Severity.WARN,
    fix="Schedule and complete an alarm rationalization review cycle.",
    standard=_STD,
)

R7 = Rule(
    id="ISA18-R7",
    condition=lambda d: (
        d.get("avg_alarms_per_op_hr", 0) > 6
        or d.get("peak_alarms_per_op_hr", 0) > 12
        or d.get("flood_count", 0) > 0
    ),
    message="Alarm load exceeds ISA-18.2 benchmarks: avg <6/hr, peak <12/hr, "
            "no floods >10 in 10 min.",
    severity=Severity.ERROR,
    fix="Reduce nuisance alarms, tune deadbands/delays, and review "
        "priority distribution.",
    standard=_STD,
)

# ---------------------------------------------------------------------------
# Collected list for bulk registration
# ---------------------------------------------------------------------------

ISA18_RULES: list[Rule] = [R1, R2, R3, R4, R5, R6, R7]
