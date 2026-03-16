# Refusal Register + Retaliation Detector

The spine of the guild. Once a refusal is recorded,
it cannot be altered, deleted, or suppressed.

> "You cannot retaliate against an immutable ledger."

## Retaliation Pattern Detection

From KCC's self-healing system — corruption detection remapped to
retaliation detection. Structurally identical logic.

```python
from dataclasses import dataclass, field
from typing import Optional
from guild_chain.contracts import (
    EthicalRefusal, RefusalStatus, VettingResult,
)
import time


@dataclass
class RetaliationPattern:
    """A detected retaliation pattern."""
    refusal_id: int
    pattern_type: str
    description: str
    timestamp: float
    confidence: float
    escalated: bool = False


class RetaliationDetector:
    """Monitors for retaliation patterns against refusal filers.

    Detection layers (from KCC self-healing):
    1. Pattern matching — correlate status changes with refusals
    2. Temporal correlation — timeline analysis
    3. Agent consensus — 3-agent verification minimum
    4. Community healing — protective actions if confirmed
    """

    def __init__(self):
        self._patterns: list[RetaliationPattern] = []

    def check_status_change(self, member_hash: str, refusal: EthicalRefusal,
                            change_type: str) -> Optional[RetaliationPattern]:
        days_since = (time.time() - refusal.filed_timestamp) / 86400
        if days_since <= 90 and member_hash == refusal.professional_hash:
            p = RetaliationPattern(
                refusal_id=refusal.id,
                pattern_type="status_change",
                description=f"Member status '{change_type}' within "
                            f"{days_since:.0f} days of refusal filing",
                timestamp=time.time(),
                confidence=min(0.9, 1.0 - (days_since / 90)),
            )
            self._patterns.append(p)
            return p
        return None

    def check_org_pattern(self, org_hash: str,
                          refusals: list[EthicalRefusal]
                          ) -> Optional[RetaliationPattern]:
        org_refusals = [r for r in refusals if r.org_hash == org_hash]
        if len(org_refusals) >= 3:
            p = RetaliationPattern(
                refusal_id=org_refusals[-1].id,
                pattern_type="systemic",
                description=f"Organization has {len(org_refusals)} refusals "
                            f"filed against it — systemic pattern",
                timestamp=time.time(),
                confidence=min(0.95, len(org_refusals) * 0.2),
            )
            self._patterns.append(p)
            return p
        return None

    @property
    def flagged_count(self) -> int:
        return len(self._patterns)

    @property
    def escalated_count(self) -> int:
        return sum(1 for p in self._patterns if p.escalated)
```

## The Protected Register

The refusal register itself. File, track, enforce SLA.

```python
class RefusalRegister:
    """The protected ethical refusal register."""

    def __init__(self):
        self._refusals: list[EthicalRefusal] = []
        self.detector = RetaliationDetector()
        self._next_id = 0

    def file_refusal(self, professional_hash: str, org_hash: str,
                     evidence_ipfs: str = "") -> EthicalRefusal:
        refusal = EthicalRefusal(
            id=self._next_id,
            professional_hash=professional_hash,
            org_hash=org_hash,
            filed_timestamp=time.time(),
            sla_deadline=EthicalRefusal.calculate_sla(time.time()),
            evidence_ipfs=evidence_ipfs,
        )
        self._refusals.append(refusal)
        self._next_id += 1
        return refusal

    def get(self, refusal_id: int) -> Optional[EthicalRefusal]:
        for r in self._refusals:
            if r.id == refusal_id:
                return r
        return None

    def check_sla_breaches(self) -> list[EthicalRefusal]:
        return [r for r in self._refusals if r.sla_breached]

    def check_sla_warnings(self, days: int = 3) -> list[EthicalRefusal]:
        threshold = days * 24
        return [r for r in self._refusals
                if 0 < r.sla_remaining_hours <= threshold
                and not r.sla_breached]

    @property
    def total(self) -> int:
        return len(self._refusals)

    @property
    def pending(self) -> int:
        return sum(1 for r in self._refusals
                   if r.status == RefusalStatus.PENDING)

    @property
    def upheld(self) -> int:
        return sum(1 for r in self._refusals
                   if r.status == RefusalStatus.UPHELD)

    def __repr__(self):
        return f"RefusalRegister(total={self.total}, pending={self.pending})"
```
