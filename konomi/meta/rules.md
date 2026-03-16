# Rule Engine

Constraints, validations, and severity levels. Rules are the enforcement mechanism across all standards.

## Severity and RuleViolation

```python
from dataclasses import dataclass, field
from typing import Optional, Callable, Any
from enum import Enum


class Severity(Enum):
    """Rule violation severity."""
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    FATAL = "fatal"


@dataclass
class RuleViolation:
    """A single rule violation found during validation."""
    rule_id: str
    severity: Severity
    message: str
    context: dict = field(default_factory=dict)
    fix: str = ""

    def __repr__(self):
        return f"[{self.severity.value}] {self.rule_id}: {self.message}"
```

## Rule

A validation rule with a callable condition that produces violations when triggered.

```python
@dataclass
class Rule:
    """A validation rule with condition and action."""
    id: str
    condition: Callable[[dict], bool]   # returns True if violation found
    message: str
    severity: Severity = Severity.WARN
    fix: str = ""
    standard: str = ""

    def check(self, data: dict) -> Optional[RuleViolation]:
        """Check data against this rule. Returns violation or None."""
        try:
            if self.condition(data):
                return RuleViolation(
                    rule_id=self.id,
                    severity=self.severity,
                    message=self.message,
                    context={"standard": self.standard},
                    fix=self.fix,
                )
        except Exception:
            pass
        return None

    def __repr__(self):
        return f"Rule({self.id}, {self.severity.value})"
```

## RuleEngine

Aggregates rules from multiple standards and runs them against data.

```python
class RuleEngine:
    """Aggregates rules from multiple standards and runs them."""

    def __init__(self):
        self.rules: list[Rule] = []

    def register(self, rule: Rule):
        """Register a rule."""
        self.rules.append(rule)

    def register_many(self, rules: list[Rule]):
        """Register multiple rules."""
        self.rules.extend(rules)

    def validate(self, data: dict,
                 standards: list[str] = None) -> list[RuleViolation]:
        """Run all rules (optionally filtered by standard) against data."""
        violations = []
        for rule in self.rules:
            if standards and rule.standard not in standards:
                continue
            v = rule.check(data)
            if v:
                violations.append(v)
        return violations

    def count_by_severity(self, violations: list[RuleViolation]) -> dict:
        """Count violations by severity level."""
        counts = {s: 0 for s in Severity}
        for v in violations:
            counts[v.severity] += 1
        return {k.value: v for k, v in counts.items()}

    def is_compliant(self, violations: list[RuleViolation]) -> bool:
        """Check if there are no error/fatal violations."""
        return not any(
            v.severity in (Severity.ERROR, Severity.FATAL)
            for v in violations
        )

    def summary(self, violations: list[RuleViolation]) -> str:
        """Generate a text summary of violations."""
        if not violations:
            return "COMPLIANT — no violations found"
        counts = self.count_by_severity(violations)
        parts = []
        for sev in ["fatal", "error", "warn", "info"]:
            if counts[sev] > 0:
                parts.append(f"{counts[sev]} {sev}")
        grade = "NON-COMPLIANT" if not self.is_compliant(violations) else "NEEDS REVIEW"
        return f"{grade} — {', '.join(parts)}"

    @property
    def rule_count(self) -> int:
        return len(self.rules)

    def __repr__(self):
        return f"RuleEngine(rules={len(self.rules)})"
```
