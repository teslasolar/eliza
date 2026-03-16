# Scanner Engine

Aggregates all standard-specific rules and runs them against code or factory configurations for standards compliance checking.

## ScanResult

```python
"""
Scanner Engine — aggregates all standard-specific rules
and runs them against code or factory configurations.
"""

import re
from dataclasses import dataclass, field
from konomi.meta.rules import Rule, RuleEngine, Severity, RuleViolation
from konomi.scanner.rules_isa88 import get_isa88_rules
from konomi.scanner.rules_isa95 import get_isa95_rules
from konomi.scanner.rules_isa18 import get_isa18_rules
from konomi.scanner.rules_isa101 import get_isa101_rules
from konomi.scanner.rules_acg import get_acg_rules


@dataclass
class ScanResult:
    """Result of a standards scan."""
    violations: list = field(default_factory=list)
    rules_checked: int = 0
    source: str = ""

    @property
    def is_compliant(self) -> bool:
        return not any(
            v.severity in (Severity.ERROR, Severity.FATAL)
            for v in self.violations
        )

    @property
    def grade(self) -> str:
        if not self.violations:
            return "COMPLIANT"
        if not self.is_compliant:
            return "NON-COMPLIANT"
        return "NEEDS REVIEW"

    def counts(self) -> dict:
        c = {"fatal": 0, "error": 0, "warn": 0, "info": 0}
        for v in self.violations:
            c[v.severity.value] += 1
        return c

    def report(self) -> str:
        """Generate text report."""
        lines = [f"Scan Result: {self.grade}"]
        lines.append(f"Rules checked: {self.rules_checked}")
        c = self.counts()
        lines.append(f"Findings: {c['error']} errors, "
                     f"{c['warn']} warnings, {c['info']} info")
        if self.violations:
            lines.append("")
            for v in sorted(self.violations,
                            key=lambda x: ["fatal", "error", "warn", "info"
                                           ].index(x.severity.value)):
                lines.append(f"  [{v.severity.value}] {v.rule_id}: {v.message}")
                if v.fix:
                    lines.append(f"    Fix: {v.fix}")
        return "\n".join(lines)
```

## Scanner

```python
class Scanner:
    """Standards compliance scanner."""

    def __init__(self, standards: list[str] = None):
        """
        Initialize scanner with selected standards.
        None = all standards enabled.
        """
        self.engine = RuleEngine()
        all_rules = []
        all_rules.extend(get_isa88_rules())
        all_rules.extend(get_isa95_rules())
        all_rules.extend(get_isa18_rules())
        all_rules.extend(get_isa101_rules())
        all_rules.extend(get_acg_rules())

        for rule in all_rules:
            if standards is None or rule.standard in standards:
                self.engine.register(rule)

    def scan_code(self, code: str) -> ScanResult:
        """Scan source code against registered rules."""
        data = {"code": code, "type": "code"}
        violations = self.engine.validate(data)
        return ScanResult(
            violations=violations,
            rules_checked=self.engine.rule_count,
            source="code",
        )

    def scan_factory(self, site) -> ScanResult:
        """Scan a factory site configuration against rules."""
        data = {
            "type": "factory",
            "site": site,
            "tags": site.tag_db.all_paths() if site.tag_db else [],
            "tag_count": site.tag_db.tag_count if site.tag_db else 0,
        }
        violations = self.engine.validate(data)
        return ScanResult(
            violations=violations,
            rules_checked=self.engine.rule_count,
            source=f"factory:{site.name}",
        )

    def scan_file(self, filepath: str) -> ScanResult:
        """Scan a file from disk."""
        with open(filepath, "r") as f:
            code = f.read()
        result = self.scan_code(code)
        result.source = filepath
        return result

    def __repr__(self):
        return f"Scanner(rules={self.engine.rule_count})"
```
