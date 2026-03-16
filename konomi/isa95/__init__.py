"""
ISA-95: Enterprise-Control System Integration Standard.

Provides dataclass-based implementations of the ISA-95 standard covering:
- 5-level Purdue hierarchy (levels)
- Equipment hierarchy & physical assets (equipment)
- Material tracking with lots/sublots (material)
- Personnel, roles, qualifications (personnel)
- Process segments (process)
- Production scheduling & performance (production)
- Inter-level data flows (data_flows)
"""

from konomi.meta.standard import Standard

# --- Levels ---
from konomi.isa95.levels import (
    Level,
    L0, L1, L2, L3, L4,
    ALL_LEVELS,
    get_level,
)

# --- Equipment ---
from konomi.isa95.equipment import (
    EquipmentState,
    EquipmentMode,
    HierarchyLevel,
    PhysicalAsset,
    Equipment,
)

# --- Material ---
from konomi.isa95.material import (
    PropertyDef,
    MaterialClass,
    SubLot,
    Material,
)

# --- Personnel ---
from konomi.isa95.personnel import (
    Qualification,
    Personnel,
)

# --- Process ---
from konomi.isa95.process import (
    ProcessParameter,
    MaterialRef,
    ProcessSegment,
)

# --- Production ---
from konomi.isa95.production import (
    ScheduleState,
    SegmentRequirement,
    SegmentActual,
    KPI,
    ProductionSchedule,
    ProductionPerformance,
)

# --- Data Flows ---
from konomi.isa95.data_flows import (
    DataFlow,
    FLOW_L4_L3, FLOW_L3_L4,
    FLOW_L3_L2, FLOW_L2_L3,
    FLOW_L2_L1, FLOW_L1_L2,
    FLOW_L1_L0, FLOW_L0_L1,
    ALL_FLOWS, DOWNWARD_FLOWS, UPWARD_FLOWS,
    flows_from, flows_to,
)

# ---------------------------------------------------------------------------
# Build the ISA-95 Standard instance
# ---------------------------------------------------------------------------

ISA95 = Standard(
    id="ISA-95",
    scope="Enterprise-Control System Integration",
    version="2018",
    hierarchy=ALL_LEVELS,
)
