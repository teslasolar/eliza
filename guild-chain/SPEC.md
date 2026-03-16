# ACG-KCC: Guild Chain Specification

> "The protected register is on-chain. Good luck retaliating against a blockchain."

**Version:** 1.0 | **Date:** March 2026 | **Network:** Permissioned PoA/PoS
**Total Supply:** 510,510 GLD | **Parent:** Konomi Cube Coin v3.0

This file is both documentation AND executable code.
Run: `python runmd.py guild-chain/SPEC.md`

---

## 1. Token Distribution

GLD is NOT a cryptocurrency. It is earned through participation, never purchased.

```python
from guild_chain.tokens import GLD_SUPPLY, DISTRIBUTION, EarnRate

print(f"Total GLD Supply: {GLD_SUPPLY:,}")
print()
for bucket in DISTRIBUTION:
    print(f"  {bucket.category.value:<16s} {bucket.amount:>8,} GLD "
          f"({bucket.pct:.0f}%) — {bucket.purpose}")
print()
print("Earn rates:")
for rate in EarnRate:
    print(f"  {rate.name:<24s} {rate.value:>4} GLD")
```

## 2. Dual-Layer Architecture

Layer 1 (PoA) is the permanent record. Layer 2 (DPoS) is real-time ops.

```python
from guild_chain.layers import Layer1, Layer2, CrossLayerBridge

l1 = Layer1()
l2 = Layer2()
bridge = CrossLayerBridge()

print(f"Layer 1: {l1.consensus.value}")
print(f"  Block time: {l1.block_time_s}s, Size: {l1.block_size_mb}MB")
print(f"  Finality: {l1.finality.value}")
print(f"  Authorities: {l1.min_authorities}-{l1.max_authorities}")
print(f"  Hardware: {l1.node_hw}")
print()
print(f"Layer 2: {l2.consensus.value}")
print(f"  Block time: {l2.block_time_s}s, TPS: {l2.throughput_tps}")
print(f"  Finality: {l2.finality.value}")
print(f"  Min stake: {l2.min_stake} GLD")
print()
print("Bridge rules:")
for event in ["ethical_refusal", "vetting_completion", "raw_transcript"]:
    print(f"  {event:<24s} → {bridge.should_bridge(event)}")
```

## 3. Guild Agents (KCC Cube Remapping)

8 vertex agents from KCC's 1000³ cube, remapped to guild operations.

```python
from guild_chain.agents import GUILD_AGENTS, TOTAL_AGENTS, OperationSlot

print(f"Total agents in network: {TOTAL_AGENTS:,}")
print(f"  8 vertex + 2,048 sub + 4,096 micro")
print()
for agent in GUILD_AGENTS:
    print(f"  Agent {agent.id} {agent.vertex} — {agent.role.value.upper()}")
    print(f"    KCC: {agent.kcc_original}")
    print(f"    ACG: {agent.guild_function}")
    if agent.slot_range:
        print(f"    Slots: {agent.slot_range}")
    print()

# Show a sample operation slot
slot = OperationSlot(slot_id=260, active=True, operation_type="ethical_refusal")
print(f"Slot {slot.slot_id}: unit={slot.owning_unit}, "
      f"agents={slot.agent_team_size}, states={slot.packml_states}")
```

## 4. Ethical Refusal Register

The spine of the guild. Once recorded, it cannot be altered, deleted, or suppressed.

```python
from guild_chain.refusal import RefusalRegister
import hashlib

register = RefusalRegister()

# File a refusal
r = register.file_refusal(
    professional_hash=hashlib.sha256(b"engineer_alice+salt").hexdigest(),
    org_hash=hashlib.sha256(b"megacorp_inc").hexdigest(),
    evidence_ipfs="QmEvidenceBundle123"
)

print(f"Refusal #{r.id} filed")
print(f"  Professional: {r.professional_hash[:16]}... (anonymized)")
print(f"  Organization: {r.org_hash[:16]}... (anonymized)")
print(f"  SLA deadline: {r.sla_remaining_hours:.0f} hours remaining")
print(f"  Status: {r.status.value}")
print(f"  Record hash: {r.record_hash[:24]}...")
print(f"  SLA breached: {r.sla_breached}")
print()

# Check SLA status
warnings = register.check_sla_warnings()
breaches = register.check_sla_breaches()
print(f"SLA warnings: {len(warnings)}, breaches: {len(breaches)}")
print(f"Register: {register}")
```

## 5. Vetting Session Contract

ELIZA sessions are tracked on L2, checkpointed to L1 on PASS.

```python
from guild_chain.contracts import VettingSession, VettingResult
import hashlib

session = VettingSession(
    id=1,
    candidate_hash=hashlib.sha256(b"candidate_bob").hexdigest(),
    model_id="SmolLM2-1.7B-Instruct"
)

print(f"Vetting session #{session.id}")
print(f"  Candidate: {session.candidate_hash[:16]}...")
print(f"  Model: {session.model_id}")
print(f"  Result: {session.result.value}")

# Complete the session
session.complete(VettingResult.PASS, "Full conversation transcript here...")
seal = session.seal

print(f"\nSession completed: {session.result.value}")
print(f"  Transcript hash: {session.transcript_hash[:24]}...")
if seal:
    print(f"  Seal issued:")
    for k, v in seal.items():
        print(f"    {k}: {v}")
```

## 6. Tag Provider Status

Ignition-style tags for the guild chain.

```python
from guild_chain.tags import create_provider

provider = create_provider()
print(f"Guild Chain Tag Provider: {provider.count} tags\n")
for path in provider.paths():
    tag = provider.get(path)
    v = tag.read()
    print(f"  [{path}] = {v.v}  ({tag.type.value}) — {tag.desc}")
```

---

## The Point

The ACG Manifesto's Principle 6 — Right and Duty to Refuse — is only as
strong as the register that protects it. ACG-KCC makes the human's refusal
un-removable. Because you can't remove a refusal that's on a blockchain
running on 50 Raspberry Pis in 50 living rooms.

The spine doesn't bend. 510,510 ⚒ ACG
