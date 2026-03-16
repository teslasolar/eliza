# GLD Token — Guild Tokens for ACG-KCC

510,510 total supply. **NOT** a cryptocurrency. **NOT** traded.
Utility token for governance, staking, and operations.
GLD is earned through participation, never purchased.

## Token Model

```python
from dataclasses import dataclass, field
from enum import Enum


GLD_SUPPLY = 510_510


class TokenAllocation(Enum):
    """GLD distribution categories."""
    FOUNDING = "founding"           # 20% — 102,102 GLD
    ACTIVE_MEMBERS = "active"       # 40% — 204,204 GLD
    OPERATIONS = "operations"       # 25% — 127,627 GLD
    FUTURE_GROWTH = "future"        # 15% — 76,577 GLD


@dataclass(frozen=True)
class AllocationBucket:
    """A token allocation bucket."""
    category: TokenAllocation
    amount: int
    pct: float
    vesting: str
    purpose: str


DISTRIBUTION = [
    AllocationBucket(TokenAllocation.FOUNDING, 102_102, 20.0,
                     "2-year linear",
                     "Governance weight for early direction"),
    AllocationBucket(TokenAllocation.ACTIVE_MEMBERS, 204_204, 40.0,
                     "Earned through participation",
                     "Reward active participation"),
    AllocationBucket(TokenAllocation.OPERATIONS, 127_627, 25.0,
                     "Released by governance vote",
                     "Node hosting, tooling, events"),
    AllocationBucket(TokenAllocation.FUTURE_GROWTH, 76_577, 15.0,
                     "Locked until 1,000 members",
                     "Scaling, partnerships, chapters"),
]
```

## Earn Rates

GLD is earned through guild participation, never purchased.

```python
class EarnRate(Enum):
    """GLD earned per activity."""
    VETTING_COMPLETE = 100      # Pass ELIZA vetting
    SERVE_AUDITOR = 500         # Per audit served
    REVIEW_PUBLICATION = 200    # Per review
    PROCESS_REFUSAL = 300       # Per refusal review
    ATTEND_SESSION = 10         # Per guild session
```

## GLD Balance

Tracks balance, staking, and voting power per member.

```python
@dataclass
class GLD:
    """A GLD token balance."""
    balance: int = 0
    staked: int = 0
    earned_total: int = 0

    def earn(self, amount: int, reason: str = ""):
        self.balance += amount
        self.earned_total += amount

    def stake(self, amount: int) -> bool:
        if amount > self.balance - self.staked:
            return False
        self.staked += amount
        return True

    def unstake(self, amount: int) -> bool:
        if amount > self.staked:
            return False
        self.staked -= amount
        return True

    @property
    def available(self) -> int:
        return self.balance - self.staked

    @property
    def voting_power(self) -> float:
        """1 GLD = 1 vote, staked = 1.5x."""
        return self.available + (self.staked * 1.5)

    def __repr__(self):
        return f"GLD(bal={self.balance}, staked={self.staked})"
```
