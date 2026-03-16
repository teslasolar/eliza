"""
Guild Contracts — GuildC contract definitions for ACG-KCC.

Core contracts:
  - EthicalRefusal: The most important contract. Protected refusal register.
  - VettingSession: ELIZA session lifecycle on-chain.
  - Certification: Conformance lifecycle (issue/suspend/revoke/expire).
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import hashlib
import time


class RefusalStatus(Enum):
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    UPHELD = "upheld"
    PARTIAL = "partial"
    NOT_UPHELD = "not_upheld"


class VettingResult(Enum):
    PENDING = "pending"
    PASS = "pass"
    NEEDS_WORK = "needs_work"


class CertStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    EXPIRED = "expired"


class CertLevel(Enum):
    CL_1 = "CL-1"
    CL_2 = "CL-2"
    CL_3 = "CL-3"


@dataclass
class EthicalRefusal:
    """On-chain ethical refusal record. Immediate L1 write."""
    id: int
    professional_hash: str      # anonymized identity
    org_hash: str               # anonymized organization
    filed_timestamp: float
    sla_deadline: float         # filed + 15 business days
    status: RefusalStatus = RefusalStatus.PENDING
    reviewer_hash: str = ""
    evidence_ipfs: str = ""     # IPFS hash of evidence bundle
    retaliation_flag: bool = False

    @staticmethod
    def calculate_sla(filed_ts: float) -> float:
        """15 business days = ~21 calendar days."""
        return filed_ts + (21 * 86400)

    @property
    def sla_remaining_hours(self) -> float:
        return max(0, (self.sla_deadline - time.time()) / 3600)

    @property
    def sla_breached(self) -> bool:
        return (time.time() > self.sla_deadline and
                self.status in (RefusalStatus.PENDING,
                                RefusalStatus.UNDER_REVIEW))

    @property
    def record_hash(self) -> str:
        raw = f"{self.id}{self.professional_hash}{self.org_hash}" \
              f"{self.filed_timestamp}{self.status.value}"
        return hashlib.sha256(raw.encode()).hexdigest()


@dataclass
class VettingSession:
    """On-chain vetting session record."""
    id: int
    candidate_hash: str
    phase: int = 0              # 0-6
    result: VettingResult = VettingResult.PENDING
    started: float = field(default_factory=time.time)
    completed: float = 0.0
    transcript_hash: str = ""   # hash of transcript, NOT transcript
    model_id: str = ""          # which WebLLM model

    def complete(self, result: VettingResult, transcript: str):
        self.result = result
        self.completed = time.time()
        self.transcript_hash = hashlib.sha256(
            transcript.encode()).hexdigest()

    @property
    def seal(self) -> Optional[dict]:
        """Generate verifiable seal if passed."""
        if self.result != VettingResult.PASS:
            return None
        return {
            "type": "ACG_VETTED_SEAL",
            "session_hash": self.transcript_hash,
            "chain": "acg-kcc-l1",
            "timestamp": self.completed,
            "model": self.model_id,
        }


@dataclass
class Certification:
    """On-chain certification record."""
    id: int
    org_hash: str
    level: CertLevel = CertLevel.CL_1
    issued: float = field(default_factory=time.time)
    expiry: float = 0.0
    auditor_hash: str = ""
    evidence_ipfs: str = ""
    status: CertStatus = CertStatus.ACTIVE

    def __post_init__(self):
        if self.expiry == 0.0:
            self.expiry = self.issued + (24 * 30 * 86400)  # 24 months

    @property
    def days_until_expiry(self) -> float:
        return max(0, (self.expiry - time.time()) / 86400)

    @property
    def needs_renewal_warning(self) -> bool:
        return self.days_until_expiry <= 60 and self.status == CertStatus.ACTIVE

    def suspend(self):
        self.status = CertStatus.SUSPENDED

    def revoke(self):
        self.status = CertStatus.REVOKED
