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

All standards are cross-walked and self-describing via UDTs.
"""

__version__ = "1.0.0"
__author__ = "ACG Guild"

from konomi.meta.standard import Standard
from konomi.meta.udt import UDT, Field
from konomi.meta.state_machine import StateMachine, Transition
from konomi.meta.entity import Entity, Relation
from konomi.meta.rules import Rule, RuleEngine
