"""
3D Vector Space Blocks — Spatial encoding of standards and knowledge.

Every piece of data gets a 3D coordinate:
  X: Domain axis     (0-1000) — what standard/area
  Y: Abstraction axis (0-1000) — raw data → principle
  Z: Lifecycle axis   (0-1000) — define → configure → runtime → audit

Similar concepts cluster in 3D space. The vector blockchain is an
immutable spatial index of all ACG knowledge.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import hashlib
import math
import time
import json


# ── Axis Mappings ─────────────────────────────────────────────────────

class DomainAxis(Enum):
    """X-axis: what domain does this data belong to?"""
    META = 0
    BASE = 50
    TAGS = 100
    FACTORY = 150
    ISA88 = 200
    ISA101 = 300
    ISA18 = 350
    ISA95 = 400
    OPCUA = 600
    SPARKPLUG = 650
    MODBUS = 700
    KPI = 750
    SCANNER = 800
    EVGPU = 850
    FEMTO = 875
    L5X = 900
    OPS = 925
    CROSSWALK = 950
    ACG = 1000


class AbstractionAxis(Enum):
    """Y-axis: how abstract is this data?"""
    REGISTER = 0           # Raw bits, registers, addresses
    VALUE = 125            # Typed values with quality
    TAG = 250              # Named data points
    STRUCTURE = 375        # UDTs, composite types
    UDT = 500              # User-defined types, schemas
    STATE_MACHINE = 625    # Behavioral models
    STANDARD = 750         # Standards definitions
    RULE = 875             # Compliance rules
    PRINCIPLE = 1000       # ACG Manifesto principles


class LifecycleAxis(Enum):
    """Z-axis: where in the lifecycle is this data?"""
    DEFINE = 0             # Design time
    CONFIGURE = 250        # Setup, parameterization
    RUNTIME = 500          # Production, live data
    MONITOR = 750          # KPIs, alarms, dashboards
    AUDIT = 1000           # Compliance, refusal register


# ── Vector ────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Vector3D:
    """A point in 3D standard space."""
    x: int   # Domain
    y: int   # Abstraction
    z: int   # Lifecycle

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def distance_to(self, other: "Vector3D") -> float:
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )

    def as_tuple(self) -> tuple[int, int, int]:
        return (self.x, self.y, self.z)

    def __repr__(self):
        return f"V({self.x}, {self.y}, {self.z})"


def encode_vector(domain: DomainAxis,
                  abstraction: AbstractionAxis,
                  lifecycle: LifecycleAxis) -> Vector3D:
    """Encode data into 3D vector space using axis enums."""
    return Vector3D(domain.value, abstraction.value, lifecycle.value)


# ── Vector Block ──────────────────────────────────────────────────────

@dataclass
class VectorBlock:
    """A block with 3D spatial coordinates in the guild chain."""
    index: int
    timestamp: float
    prev_hash: str
    data: dict                      # Arbitrary JSON-serializable payload
    vector: Vector3D                # 3D position in standard space
    layer: int = 1                  # 1 (permanent) or 2 (operations)
    validator: str = ""
    category: str = ""              # e.g., "standard", "principle", "tag"

    @property
    def data_hash(self) -> str:
        raw = json.dumps(self.data, sort_keys=True, default=str)
        return hashlib.sha256(raw.encode()).hexdigest()

    @property
    def hash(self) -> str:
        raw = (f"{self.index}{self.timestamp}{self.prev_hash}"
               f"{self.data_hash}{self.vector.x}{self.vector.y}{self.vector.z}"
               f"{self.layer}{self.validator}")
        return hashlib.sha256(raw.encode()).hexdigest()

    def __repr__(self):
        return (f"VBlock #{self.index} {self.vector} "
                f"[{self.category}] {self.hash[:12]}…")


# ── Vector Chain ──────────────────────────────────────────────────────

@dataclass
class VectorChain:
    """A blockchain of 3D vector blocks."""
    blocks: list[VectorBlock] = field(default_factory=list)

    def genesis(self) -> VectorBlock:
        """Create the genesis block at the center of the space."""
        b = VectorBlock(
            index=0,
            timestamp=time.time(),
            prev_hash="0" * 64,
            data={"type": "genesis", "message": "ACG-KCC Vector Genesis",
                  "supply": 510_510},
            vector=Vector3D(500, 500, 500),
            layer=1,
            validator="genesis",
            category="genesis",
        )
        self.blocks.append(b)
        return b

    def add(self, data: dict, vector: Vector3D,
            category: str = "", layer: int = 1,
            validator: str = "auto") -> VectorBlock:
        """Add a new vector block to the chain."""
        prev = self.blocks[-1].hash if self.blocks else "0" * 64
        b = VectorBlock(
            index=len(self.blocks),
            timestamp=time.time(),
            prev_hash=prev,
            data=data,
            vector=vector,
            layer=layer,
            validator=validator,
            category=category,
        )
        self.blocks.append(b)
        return b

    @property
    def height(self) -> int:
        return len(self.blocks)

    def verify(self) -> bool:
        """Verify chain integrity."""
        for i in range(1, len(self.blocks)):
            if self.blocks[i].prev_hash != self.blocks[i - 1].hash:
                return False
        return True

    def query_radius(self, center: Vector3D, radius: float) -> list[VectorBlock]:
        """Find all blocks within a radius of a 3D point."""
        return [b for b in self.blocks
                if b.vector.distance_to(center) <= radius]

    def query_axis(self, axis: str, low: int, high: int) -> list[VectorBlock]:
        """Filter blocks by an axis range."""
        return [b for b in self.blocks
                if low <= getattr(b.vector, axis) <= high]

    def nearest(self, point: Vector3D, n: int = 5) -> list[VectorBlock]:
        """Find the N nearest blocks to a point."""
        ranked = sorted(self.blocks,
                        key=lambda b: b.vector.distance_to(point))
        return ranked[:n]


# ── Standard Encoders ─────────────────────────────────────────────────

# Pre-built vectors for encoding KONOMI packages
KONOMI_VECTORS = {
    "meta":      encode_vector(DomainAxis.META, AbstractionAxis.STANDARD, LifecycleAxis.DEFINE),
    "base":      encode_vector(DomainAxis.BASE, AbstractionAxis.VALUE, LifecycleAxis.DEFINE),
    "tags":      encode_vector(DomainAxis.TAGS, AbstractionAxis.TAG, LifecycleAxis.RUNTIME),
    "factory":   encode_vector(DomainAxis.FACTORY, AbstractionAxis.STRUCTURE, LifecycleAxis.CONFIGURE),
    "isa88":     encode_vector(DomainAxis.ISA88, AbstractionAxis.STATE_MACHINE, LifecycleAxis.RUNTIME),
    "isa95":     encode_vector(DomainAxis.ISA95, AbstractionAxis.STANDARD, LifecycleAxis.CONFIGURE),
    "isa18":     encode_vector(DomainAxis.ISA18, AbstractionAxis.TAG, LifecycleAxis.MONITOR),
    "isa101":    encode_vector(DomainAxis.ISA101, AbstractionAxis.STRUCTURE, LifecycleAxis.CONFIGURE),
    "opcua":     encode_vector(DomainAxis.OPCUA, AbstractionAxis.UDT, LifecycleAxis.RUNTIME),
    "sparkplug": encode_vector(DomainAxis.SPARKPLUG, AbstractionAxis.TAG, LifecycleAxis.RUNTIME),
    "modbus":    encode_vector(DomainAxis.MODBUS, AbstractionAxis.REGISTER, LifecycleAxis.RUNTIME),
    "kpi":       encode_vector(DomainAxis.KPI, AbstractionAxis.UDT, LifecycleAxis.MONITOR),
    "crosswalk": encode_vector(DomainAxis.CROSSWALK, AbstractionAxis.STANDARD, LifecycleAxis.DEFINE),
    "scanner":   encode_vector(DomainAxis.SCANNER, AbstractionAxis.RULE, LifecycleAxis.AUDIT),
    "evgpu":     encode_vector(DomainAxis.EVGPU, AbstractionAxis.VALUE, LifecycleAxis.RUNTIME),
    "femto":     encode_vector(DomainAxis.FEMTO, AbstractionAxis.STRUCTURE, LifecycleAxis.RUNTIME),
    "l5x":       encode_vector(DomainAxis.L5X, AbstractionAxis.UDT, LifecycleAxis.DEFINE),
    "ops":       encode_vector(DomainAxis.OPS, AbstractionAxis.STRUCTURE, LifecycleAxis.RUNTIME),
}

# ACG Manifesto principle vectors — all at x=1000, y=1000
ACG_VECTORS = {
    "principle_1_innovation":    Vector3D(1000, 1000, 0),     # Define-phase
    "principle_2_quality":       Vector3D(1000, 1000, 250),   # Configure-phase
    "principle_3_safety":        Vector3D(1000, 1000, 500),   # Runtime-phase
    "principle_4_human":         Vector3D(1000, 1000, 625),   # Runtime/Monitor
    "principle_5_consent":       Vector3D(1000, 1000, 750),   # Monitor-phase
    "principle_6_refuse":        Vector3D(1000, 1000, 1000),  # Audit-phase
}


def build_standard_chain() -> VectorChain:
    """Build a chain pre-loaded with all KONOMI standards and ACG principles."""
    chain = VectorChain()
    chain.genesis()

    # Encode all KONOMI packages
    for pkg, vec in KONOMI_VECTORS.items():
        chain.add(
            data={"type": "standard", "package": f"konomi.{pkg}"},
            vector=vec,
            category="standard",
            validator="konomi",
        )

    # Encode ACG principles
    principles = {
        "principle_1_innovation": "Embracing Innovation — explore but verify",
        "principle_2_quality": "Demanding Quality — rigorous verification",
        "principle_3_safety": "Ensuring Safety — proper harnesses",
        "principle_4_human": "Protecting Humans — psychological safety",
        "principle_5_consent": "Informed Consent — transparency required",
        "principle_6_refuse": "Right to Refuse — ethical obligation",
    }
    for key, desc in principles.items():
        chain.add(
            data={"type": "principle", "key": key, "description": desc},
            vector=ACG_VECTORS[key],
            category="principle",
            validator="acg",
        )

    return chain
