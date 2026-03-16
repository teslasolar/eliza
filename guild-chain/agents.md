# Guild Agents — KCC Cube Remapping

KCC's 8 vertex agents from the 1000³ computational cube become
6 guild unit agents + 2 system agents. 512 sub-cubes become operation slots.

## Agent Model

```python
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class AgentRole(Enum):
    VETTING = "vetting"             # Agent 0 [0,0,0]
    CERTIFICATION = "certification"  # Agent 1 [999,0,0]
    PUBLISHING = "publishing"        # Agent 2 [999,999,0]
    REFUSAL = "refusal"             # Agent 3 [0,999,0] — the guardian
    AUDIT = "audit"                 # Agent 4 [0,0,999]
    MEMBERSHIP = "membership"       # Agent 5 [999,0,999]
    RESOURCE_MGR = "resource_mgr"   # Agent 6 [999,999,999]
    ERROR_CORRECT = "error_correct"  # Agent 7 [0,999,999]


@dataclass(frozen=True)
class CubeVertex:
    """Position in the KCC cube."""
    x: int
    y: int
    z: int

    def __str__(self):
        return f"[{self.x},{self.y},{self.z}]"


@dataclass
class GuildAgent:
    """A vertex agent in the guild chain."""
    id: int
    role: AgentRole
    vertex: CubeVertex
    kcc_original: str
    guild_function: str
    accuracy: str = ""
    slot_range: str = ""

    def __repr__(self):
        return f"Agent{self.id}({self.role.value}, {self.vertex})"
```

## The 8 Guild Agents

| Agent | Vertex | KCC Function | ACG-KCC Function | Slots |
|-------|--------|-------------|------------------|-------|
| 0 | [0,0,0] | Pattern Recognition | ELIZA coordinator | 000-127 |
| 1 | [999,0,0] | NLP Processing | Certification review | 128-191 |
| 2 | [999,999,0] | Visual Processing | Publishing + formatting | 192-255 |
| 3 | [0,999,0] | Reasoning Engine | **Refusal guardian** | 256-319 |
| 4 | [0,0,999] | Memory Management | Audit + evidence | 320-383 |
| 5 | [999,0,999] | Communication Hub | Membership + events | 384-511 |
| 6 | [999,999,999] | Resource Manager | Load balancing | System |
| 7 | [0,999,999] | Error Correction | Self-healing + SLA | System |

```python
GUILD_AGENTS = [
    GuildAgent(0, AgentRole.VETTING, CubeVertex(0, 0, 0),
               "Pattern Recognition (96.7%)",
               "ELIZA coordinator — candidate response analysis",
               "96.7%", "000-127"),
    GuildAgent(1, AgentRole.CERTIFICATION, CubeVertex(999, 0, 0),
               "NLP Processing (98.2% F1)",
               "Document review + evidence analysis + conformance",
               "98.2%", "128-191"),
    GuildAgent(2, AgentRole.PUBLISHING, CubeVertex(999, 999, 0),
               "Visual Processing (94.3%)",
               "Document formatting + manifesto alignment",
               "94.3%", "192-255"),
    GuildAgent(3, AgentRole.REFUSAL, CubeVertex(0, 999, 0),
               "Reasoning Engine (logic trees)",
               "Refusal validity + retaliation detection + SLA enforcement",
               "", "256-319"),
    GuildAgent(4, AgentRole.AUDIT, CubeVertex(0, 0, 999),
               "Memory Management (256GB)",
               "Evidence archive + retrieval + compliance history",
               "", "320-383"),
    GuildAgent(5, AgentRole.MEMBERSHIP, CubeVertex(999, 0, 999),
               "Communication Hub (10k msg/s)",
               "Member lifecycle + cross-unit event bus routing",
               "", "384-511"),
    GuildAgent(6, AgentRole.RESOURCE_MGR, CubeVertex(999, 999, 999),
               "Resource Management",
               "Load balancing across units + node health monitoring",
               "", ""),
    GuildAgent(7, AgentRole.ERROR_CORRECT, CubeVertex(0, 999, 999),
               "Error Correction (99.99%)",
               "Self-healing for all units + SLA breach detection",
               "99.99%", ""),
]
```

## Operation Slots (512 Sub-Cubes)

Each slot is a container for one active guild work item.

```python
@dataclass
class OperationSlot:
    """One of 512 sub-cube operation slots."""
    slot_id: int
    agent_team_size: int = 4
    packml_states: int = 17
    active: bool = False
    operation_type: str = ""

    @property
    def owning_unit(self) -> str:
        if self.slot_id < 128:
            return "VETTING"
        elif self.slot_id < 192:
            return "CERTIFY"
        elif self.slot_id < 256:
            return "PUBLISH"
        elif self.slot_id < 320:
            return "REFUSAL"
        elif self.slot_id < 384:
            return "AUDIT"
        else:
            return "MEMBERSHIP"


TOTAL_AGENTS = (
    8 +             # vertex agents
    512 * 4 +       # sub-agents
    512 * 8          # micro-agents
)  # = 6,152
```
