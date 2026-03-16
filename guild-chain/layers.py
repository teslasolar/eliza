"""
Dual-Layer Consensus — L1 Authority (PoA) + L2 Operations (DPoS).

L1: Permanent record. Immutable. Refusals, certs, membership.
    Raspberry Pi capable. 60s blocks. 5-11 authority nodes.

L2: Real-time ops. Fast. Vetting sessions, PackML state, events.
    5s blocks. 1000 TPS. Any staking member can validate.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import hashlib
import time


class ConsensusType(Enum):
    POA = "Proof of Authority"
    DPOS = "Delegated Proof of Stake"


class BlockFinality(Enum):
    INSTANT = "instant"     # L1: 1 block with 2/3 consensus
    FAST = "fast"           # L2: 2 blocks (~10 seconds)


@dataclass
class Block:
    """A block on either layer."""
    index: int
    timestamp: float
    prev_hash: str
    data_hash: str
    layer: int                      # 1 or 2
    validator: str = ""
    nonce: int = 0

    @property
    def hash(self) -> str:
        raw = f"{self.index}{self.timestamp}{self.prev_hash}" \
              f"{self.data_hash}{self.layer}{self.validator}{self.nonce}"
        return hashlib.sha256(raw.encode()).hexdigest()


@dataclass
class Layer1:
    """Authority Chain — permanent record."""
    consensus: ConsensusType = ConsensusType.POA
    block_time_s: int = 60
    block_size_mb: int = 1
    finality: BlockFinality = BlockFinality.INSTANT
    min_authorities: int = 5
    max_authorities: int = 11
    blocks: list[Block] = field(default_factory=list)

    purpose: str = (
        "Immutable storage: ethical refusals (ACG-R-002), "
        "certifications, membership records, governance votes, "
        "audit findings, published document hashes"
    )
    node_hw: str = "Raspberry Pi 4 (4GB RAM), 32GB SD card"

    def genesis(self):
        """Create genesis block."""
        b = Block(0, time.time(), "0" * 64,
                  hashlib.sha256(b"ACG-KCC Genesis").hexdigest(), 1,
                  "genesis")
        self.blocks.append(b)
        return b

    def add_block(self, data_hash: str, validator: str) -> Block:
        prev = self.blocks[-1].hash if self.blocks else "0" * 64
        b = Block(len(self.blocks), time.time(), prev, data_hash, 1,
                  validator)
        self.blocks.append(b)
        return b

    @property
    def height(self) -> int:
        return len(self.blocks)


@dataclass
class Layer2:
    """Operations Chain — real-time."""
    consensus: ConsensusType = ConsensusType.DPOS
    block_time_s: int = 5
    throughput_tps: int = 1000
    finality: BlockFinality = BlockFinality.FAST
    min_stake: int = 100            # GLD
    checkpoint_freq: int = 50       # L2 blocks per L1 checkpoint
    blocks: list[Block] = field(default_factory=list)

    purpose: str = (
        "Real-time: ELIZA vetting sessions, PackML state changes, "
        "event bus, SLA timers, member activity, reputation"
    )

    def add_block(self, data_hash: str, validator: str) -> Block:
        prev = self.blocks[-1].hash if self.blocks else "0" * 64
        b = Block(len(self.blocks), time.time(), prev, data_hash, 2,
                  validator)
        self.blocks.append(b)
        return b

    @property
    def height(self) -> int:
        return len(self.blocks)

    def needs_checkpoint(self) -> bool:
        return self.height > 0 and self.height % self.checkpoint_freq == 0


@dataclass
class CrossLayerBridge:
    """Bridges L2 → L1. Ethical refusals bypass checkpoint queue."""
    checkpoint_freq: int = 50       # ~4 minutes
    always_immediate: tuple = (
        "ethical_refusal",
        "certification_change",
        "membership_change",
        "governance_result",
    )
    batched: tuple = (
        "vetting_completion",
        "audit_summary",
        "packml_snapshot",
    )
    never_on_l1: tuple = (
        "raw_transcript",
        "agent_chatter",
        "temp_state",
    )

    def should_bridge(self, event_type: str) -> str:
        """Returns: 'immediate', 'batched', or 'never'."""
        if event_type in self.always_immediate:
            return "immediate"
        if event_type in self.batched:
            return "batched"
        return "never"
