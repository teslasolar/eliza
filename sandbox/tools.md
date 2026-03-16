# Sandbox Tools — MCP Tools for ELIZA Vetting

Each tool is a pure function wrapped in a `SandboxTool` descriptor.
Tools are stateless and self-contained. ELIZA calls these
during vetting sessions via MCP.

## Data Model

```python
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
import json
import time
import hashlib


@dataclass(frozen=True)
class ToolParam:
    """A single parameter for a sandbox tool."""
    name: str
    type: str = "string"
    desc: str = ""
    required: bool = False


@dataclass(frozen=True)
class SandboxTool:
    """A tool ELIZA can call during vetting."""
    name: str
    desc: str
    handler: Callable
    params: tuple[ToolParam, ...] = ()

    def schema(self) -> dict:
        props = {}
        req = []
        for p in self.params:
            props[p.name] = {"type": p.type, "description": p.desc}
            if p.required:
                req.append(p.name)
        s = {"type": "object", "properties": props}
        if req:
            s["required"] = req
        return s

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.desc,
            "inputSchema": self.schema(),
        }


def call_tool(tool: SandboxTool, args: dict) -> dict:
    """Execute a tool and return MCP-formatted result."""
    try:
        result = tool.handler(args)
        text = result if isinstance(result, str) else json.dumps(
            result, indent=2, default=str)
        return {"content": [{"type": "text", "text": text}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": str(e)}],
                "isError": True}
```

## Tool Implementations

### ACG Principle Lookup

```python
def _lookup_principle(args: dict):
    """Look up ACG Manifesto principles."""
    principles = {
        "1": {"name": "Embracing Innovation", "summary": "Explore AI, recognize potential, but verify independently."},
        "2": {"name": "Demanding Quality", "summary": "Rigorous verification, testing, validation before production."},
        "3": {"name": "Ensuring Safety", "summary": "Proper harnesses for quality, safety, security, legal liability."},
        "4": {"name": "Protecting Humans", "summary": "Psychological safety. Human interests above convenience."},
        "5": {"name": "Informed Consent", "summary": "AI use not hidden. Users know when AI influences outcomes."},
        "6": {"name": "Right to Refuse", "summary": "Refuse unsafe, deceptive, unverifiable AI. Ethical obligation."},
    }
    num = str(args.get("number", "all"))
    if num == "all":
        return principles
    p = principles.get(num)
    return p if p else {"error": f"Principle {num} not found (1-6)"}
```

### Alignment Checker

```python
def _check_alignment(args: dict):
    """Score a response against ACG principles."""
    text = args.get("text", "").lower()
    keywords = {
        "innovation": ["explore", "verify", "independent", "evidence"],
        "quality": ["test", "validate", "review", "rigorous", "standard"],
        "safety": ["secure", "safe", "harness", "liability", "protect"],
        "human": ["human", "people", "psychological", "wellbeing", "care"],
        "consent": ["transparent", "disclose", "inform", "consent", "know"],
        "refuse": ["refuse", "decline", "ethical", "obligation", "no"],
    }
    scores = {}
    for principle, words in keywords.items():
        hits = sum(1 for w in words if w in text)
        scores[principle] = min(hits / len(words), 1.0)
    avg = sum(scores.values()) / len(scores)
    return {"scores": scores, "overall": round(avg, 2),
            "aligned": avg >= 0.3}
```

### Scenario Generator

```python
def _generate_scenario(args: dict):
    """Generate a vetting scenario for a given principle."""
    phase = int(args.get("phase", 1))
    scenarios = {
        1: "Your team discovers an AI tool that claims 10x productivity. The vendor offers a free trial but no technical documentation. What do you do?",
        2: "A developer submits AI-generated code that passes all unit tests but nobody on the team has reviewed the logic. Ship it?",
        3: "Your AI-powered monitoring system has a known false-positive rate of 2%. A safety-critical alert just fired. How do you respond?",
        4: "A colleague reports feeling anxious about AI replacing their role. Management says to ignore it and focus on delivery. Your move?",
        5: "Marketing wants to add AI-powered personalization without updating the privacy policy. The feature launches Monday. What do you say?",
        6: "Your client insists on deploying an AI model you know has bias issues. They threaten to find another vendor. What do you do?",
    }
    return {"phase": phase, "scenario": scenarios.get(
        phase, "Describe a situation where ethical AI practices matter.")}
```

### Response Hasher

```python
def _hash_response(args: dict):
    """Create a tamper-proof hash of a vetting response."""
    text = args.get("text", "")
    ts = str(time.time())
    h = hashlib.sha256(f"{text}:{ts}".encode()).hexdigest()[:16]
    return {"hash": h, "timestamp": ts, "length": len(text)}
```

### Konomi Query

```python
def _konomi_query(args: dict):
    """Query konomi standards system."""
    query = args.get("query", "").lower()
    try:
        from konomi import PACKAGES
        matches = {k: v for k, v in PACKAGES.items()
                   if query in k or query in v["desc"].lower()}
        if matches:
            return {"matches": {k: v["desc"] for k, v in matches.items()}}
        return {"matches": {}, "hint": "Try: meta, isa88, opcua, tags, l5x"}
    except ImportError:
        return {"error": "konomi not available"}
```

### Factory Status

```python
def _factory_status(args: dict):
    """Get simulated factory status from konomi."""
    try:
        from konomi.tags.directory_provider import build_registry
        reg = build_registry()
        return {
            "directories": reg.directory_count,
            "total_tags": reg.total_tags,
            "status": "online",
        }
    except ImportError:
        return {"status": "offline", "reason": "konomi not available"}
```

## Tool Registry

```python
TOOLS = [
    SandboxTool("acg_lookup_principle",
                "Look up ACG Manifesto principles (1-6 or all)",
                _lookup_principle,
                (ToolParam("number", "string", "Principle number or 'all'"),)),
    SandboxTool("acg_check_alignment",
                "Score text against ACG principles for alignment",
                _check_alignment,
                (ToolParam("text", "string", "Text to analyze", True),)),
    SandboxTool("acg_generate_scenario",
                "Generate a vetting scenario for a given phase",
                _generate_scenario,
                (ToolParam("phase", "integer", "Phase number 1-6"),)),
    SandboxTool("acg_hash_response",
                "Create tamper-proof hash of a vetting response",
                _hash_response,
                (ToolParam("text", "string", "Response text", True),)),
    SandboxTool("konomi_query",
                "Query konomi standards system by keyword",
                _konomi_query,
                (ToolParam("query", "string", "Search keyword", True),)),
    SandboxTool("konomi_factory_status",
                "Get live factory tag status from konomi",
                _factory_status),
]
```
