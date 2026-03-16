"""ISA-18.2 Alarm Management scan rules."""

import re
from konomi.meta.rules import Rule, Severity


def get_isa18_rules() -> list[Rule]:
    return [
        Rule(
            id="A18-001",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'alarm.*(?:append|add|push|create|new)\s*\(',
                               d.get("code", ""), re.I)) and
                not bool(re.search(r'priority|severity|level|P[1-4]',
                                   d.get("code", ""), re.I))
            ),
            message="Alarm created without priority. ISA-18.2 requires P1-P4 priority on every alarm.",
            severity=Severity.ERROR,
            fix="Assign priority: P1=Emergency(<1min), P2=High(<10min), P3=Medium(<1hr), P4=Low(shift).",
            standard="ISA-18.2",
        ),
        Rule(
            id="A18-002",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'alarm|alert', d.get("code", ""), re.I)) and
                not bool(re.search(r'response|action|procedure|instruction',
                                   d.get("code", ""), re.I))
            ),
            message="Alarms without actionable response procedures. ISA-18.2 R3: every alarm must be actionable.",
            severity=Severity.ERROR,
            fix="Document operator response for each alarm: what to check, what to do.",
            standard="ISA-18.2",
        ),
        Rule(
            id="A18-003",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'alarm', d.get("code", ""), re.I)) and
                not bool(re.search(r'ack|acknowledge|shelv|suppress|alarm.*state',
                                   d.get("code", ""), re.I))
            ),
            message="No alarm state lifecycle management. ISA-18.2 requires NORMAL→UNACK→ACKED→RTN_UNACK states.",
            severity=Severity.WARN,
            standard="ISA-18.2",
        ),
        Rule(
            id="A18-004",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(
                    r'(?:print|console\.log|System\.out)\s*\(.*(?:alarm|alert|warning)',
                    d.get("code", ""), re.I))
            ),
            message="Print/console used for alarm notification. Use structured alarm management system.",
            severity=Severity.WARN,
            fix="Replace print with alarm management system that tracks state, priority, and acknowledgment.",
            standard="ISA-18.2",
        ),
        Rule(
            id="A18-005",
            condition=lambda d: (
                d.get("type") == "factory" and
                any("ALM_" in t for t in d.get("tags", [])) and
                not any("ALM_Summary" in t for t in d.get("tags", []))
            ),
            message="Factory has alarms but no alarm summary tags. ISA-18.2 requires area-level alarm overview.",
            severity=Severity.INFO,
            standard="ISA-18.2",
        ),
    ]
