# Guild Chain Academy

ACG-KCC: Konomi Cube Coin Private Fork — immutable blockchain for ethical refusals, vetting records, and guild operations.

## What You'll Learn

- Dual-layer blockchain architecture (PoA Layer 1 + DPoS Layer 2)
- The Ethical Refusal Register — un-removable on-chain records
- GLD token economics (earned, never purchased)
- 3D vector space blocks for encoding standards data
- 8 vertex agents from the KCC cube topology
- Running nodes on Raspberry Pi hardware

## Prerequisites

- Understanding of blockchain fundamentals (blocks, hashing, consensus)
- The ACG Manifesto, especially Principle 6 (Right to Refuse)
- Python 3.10+ for running the chain locally

## Key Concepts

**Dual Layer**: L1 (Proof of Authority) is the permanent record — ethical refusals, certifications, governance votes. L2 (Delegated Proof of Stake) handles real-time operations — vetting sessions, events, PackML state. The CrossLayerBridge decides what escalates.

**Ethical Refusal Register**: The spine of the guild. When a professional files a refusal (Principle 6), it goes on-chain permanently. Cannot be deleted, altered, or suppressed. SLA tracking ensures the organization responds within 48 hours.

**GLD Token**: 510,510 total supply. NOT a cryptocurrency — earned through participation (100 GLD for passing vetting, 300 GLD for processing a refusal review). Used for governance voting (staked = 1.5x power) and L2 validation (min 100 GLD stake).

**3D Vector Blocks**: Standards, code, and knowledge are encoded into 3D coordinate vectors (x, y, z). Each dimension maps to a semantic axis. Blocks form a spatial index — similar standards cluster together in 3D space.

**8 Vertex Agents**: Remapped from KCC's 1000³ cube geometry. Each vertex agent has a guild role: Vetting Conductor, Refusal Guardian, Standards Auditor, Membership Registrar, etc.

## Architecture

- `layers.py` — Block, Layer1, Layer2, CrossLayerBridge
- `tokens.py` — GLD token, distribution, earn rates
- `agents.py` — 8 vertex agents, operation slots
- `contracts.py` — VettingSession, EthicalRefusal, Certification
- `refusal.py` — RefusalRegister, RetaliationDetector
- `tags.py` — Ignition-style tag provider for chain metrics
- `vectors.py` — 3D vector block encoding (NEW)
