"""
KONOMI STANDARD — Self-Defining Industrial Standards System
ACG Guild Platform · AI Craftspeople Guild

A complete industrial standards implementation covering:
- ISA-95: Enterprise/Control Integration
- ISA-88: Batch Control
- ISA-101: HMI Design
- ISA-18.2: Alarm Management
- OPC-UA: Industrial Communication
- MQTT/Sparkplug: Lightweight Pub/Sub
- Modbus: Field Protocol
- KPIs: Performance Metrics
- L5X: Rockwell PLC Compiler
- CLI/API/MCP: Unified Operations Layer

All standards are cross-walked and self-describing via UDTs.
"""

__version__ = "1.0.0"
__author__ = "ACG Guild"

from konomi.meta.standard import Standard
from konomi.meta.udt import UDT, Field
from konomi.meta.state_machine import StateMachine, Transition
from konomi.meta.entity import Entity, Relation
from konomi.meta.rules import Rule, RuleEngine

# ── Subpackage Registry ─────────────────────────────────────────────

PACKAGES = {
    "meta": {
        "desc": "Layer 0: Meta-Standard — how standards define themselves",
        "provides": ["Standard", "UDT", "Field", "StateMachine",
                     "Transition", "Entity", "Relation", "Rule", "RuleEngine"],
    },
    "base": {
        "desc": "Primitive types: identifiers, timestamps, quality, values",
        "provides": ["Identifier", "TagPath", "Timestamp", "Quality",
                     "QualityFlags", "Value", "Range", "Quantity", "Status"],
    },
    "tags": {
        "desc": "Tag system — the nervous system of the factory",
        "provides": ["TagProvider", "Tag", "TagType", "ProcessTags",
                     "EquipmentTags", "BatchTags", "AlarmTags",
                     "FactoryTagDatabase"],
    },
    "factory": {
        "desc": "Factory hierarchy: Site → Area → Line → Unit + simulation",
        "provides": ["Site", "Area", "Line", "Unit", "SimEngine"],
    },
    "isa88": {
        "desc": "ISA-88 Batch Control: procedures, recipes, states",
        "provides": ["BatchControl", "Procedure", "Recipe", "BatchStates"],
    },
    "isa95": {
        "desc": "ISA-95 Enterprise/Control Integration: equipment, production",
        "provides": ["Equipment", "Production", "Material", "Personnel"],
    },
    "isa18": {
        "desc": "ISA-18.2 Alarm Management: alarm lifecycle, priorities",
        "provides": ["Alarm", "AlarmPriority", "AlarmState", "AlarmShelving"],
    },
    "isa101": {
        "desc": "ISA-101 HMI Design: screens, elements, navigation",
        "provides": ["HMIScreen", "HMIElement", "HMINavigation"],
    },
    "opcua": {
        "desc": "OPC-UA Industrial Communication: nodes, methods, subscriptions",
        "provides": ["NodeClass", "AccessLevel", "OPCNode", "OPCVariable",
                     "OPCMethod", "AddressSpace", "Subscription", "COMPANIONS"],
    },
    "sparkplug": {
        "desc": "MQTT/Sparkplug B: topics, payloads, metrics, QoS",
        "provides": ["MessageType", "SparkplugTopic", "SparkplugPayload",
                     "SparkplugMetric", "SparkplugDataType", "QoSLevel"],
    },
    "modbus": {
        "desc": "Modbus field protocol: registers, function codes, data types",
        "provides": ["RegisterType", "RegisterDef", "ModbusDataType",
                     "ModbusMap", "FunctionCode", "ModbusException"],
    },
    "kpi": {
        "desc": "KPI metrics: OEE, energy, production, reliability",
        "provides": ["OEE", "Energy", "Production", "Reliability"],
    },
    "crosswalk": {
        "desc": "Cross-standard mappings between ISA-88/95/18/101",
        "provides": ["Crosswalk", "Mapping", "CrosswalkEngine"],
    },
    "scanner": {
        "desc": "Standards compliance scanning engine + rule sets",
        "provides": ["Scanner", "ScanResult", "ScanEngine"],
    },
    "evgpu": {
        "desc": "eVGPU — CPU-based compute for edge inference",
        "provides": ["eVGPU", "Tensor"],
    },
    "femto": {
        "desc": "FemtoLLM — tiny ML model for industrial classification",
        "provides": ["FemtoLLM"],
    },
    "l5x": {
        "desc": "L5X Compiler — Rockwell PLC program generation",
        "provides": ["L5XCompiler", "L5XProgram", "Rung", "Instruction",
                     "L5XDataType", "L5XTag", "L5XTask"],
    },
    "ops": {
        "desc": "CLI / REST API / MCP wrappers for directory operations",
        "provides": ["CLI", "APIServer", "MCPProvider", "DirectoryOps"],
    },
}


def list_packages() -> dict:
    """Return the full subpackage registry."""
    return dict(PACKAGES)


def describe() -> str:
    """Human-readable summary of all KONOMI subpackages."""
    lines = ["KONOMI — Self-Defining Industrial Standards System", ""]
    for name, info in PACKAGES.items():
        lines.append(f"  konomi.{name:<12s}  {info['desc']}")
        provides = ", ".join(info["provides"][:4])
        if len(info["provides"]) > 4:
            provides += f" … +{len(info['provides']) - 4} more"
        lines.append(f"  {'':12s}       └── {provides}")
    return "\n".join(lines)
