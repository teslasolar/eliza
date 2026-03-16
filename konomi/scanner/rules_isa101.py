"""ISA-101 HMI Design scan rules."""

import re
from konomi.meta.rules import Rule, Severity


def get_isa101_rules() -> list[Rule]:
    return [
        Rule(
            id="H101-001",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'hmi|display|screen|graphic|dashboard|gui',
                               d.get("code", ""), re.I)) and
                bool(re.search(r'[\'"]#[0-9a-fA-F]{3,8}[\'"]|color\s*[:=]\s*[\'"](?:red|green|blue)',
                               d.get("code", ""), re.I))
            ),
            message="Hardcoded color values in HMI/display code. ISA-101 R1: no hardcoded values in graphics.",
            severity=Severity.WARN,
            fix="Use centralized style definitions and bind to ISA-101 color meanings.",
            standard="ISA-101",
        ),
        Rule(
            id="H101-002",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'hmi|screen|display|dashboard',
                               d.get("code", ""), re.I)) and
                not bool(re.search(r'overview|area.*view|unit.*view|detail|layer|level.*[1-5]',
                                   d.get("code", ""), re.I))
            ),
            message="HMI code without layer hierarchy. ISA-101: L1 Overview→L2 Area→L3 Unit→L4 Detail→L5 Support.",
            severity=Severity.INFO,
            standard="ISA-101",
        ),
        Rule(
            id="H101-003",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'button|control|command|setpoint.*input',
                               d.get("code", ""), re.I)) and
                bool(re.search(r'(?:critical|emergency|shutdown|trip)',
                               d.get("code", ""), re.I)) and
                not bool(re.search(r'confirm|dialog|are.*you.*sure|verification',
                                   d.get("code", ""), re.I))
            ),
            message="Critical command without confirmation dialog. ISA-101 R8: confirmation for critical commands.",
            severity=Severity.ERROR,
            fix="Add confirmation dialog before executing critical/emergency commands.",
            standard="ISA-101",
        ),
        Rule(
            id="H101-004",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'(?:ip\s*[:=]|address\s*[:=]|register\s*\[)',
                               d.get("code", ""), re.I)) and
                bool(re.search(r'hmi|display|graphic|widget',
                               d.get("code", ""), re.I))
            ),
            message="Direct address binding in HMI. ISA-101 R2: bind to tag path, not direct address.",
            severity=Severity.WARN,
            fix="Use tag paths (Area_Unit_Module_Point) instead of direct IP/register addresses.",
            standard="ISA-101",
        ),
    ]
