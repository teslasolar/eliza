# Dual-Layer Blockchain Architecture

## Why Two Layers?

Not everything needs to be permanent. A vetting session transcript doesn't need the same guarantees as an ethical refusal record. Two layers, two purposes:

## Layer 1 — Proof of Authority

```javascript
const L1 = {
  consensus: "Proof of Authority (PoA)",
  blockTime: "60 seconds",
  blockSize: "1 MB",
  finality: "instant (2/3 authority consensus)",
  authorities: "5-11 nodes",
  hardware: "Raspberry Pi 4 (4GB RAM, 32GB SD)",
  purpose: [
    "Ethical refusals (immutable)",
    "Certifications",
    "Membership records",
    "Governance votes",
    "Published document hashes",
  ],
};

console.log("L1:", L1.consensus);
console.log("Hardware:", L1.hardware);
L1.purpose.forEach(p => console.log("  •", p));
```

L1 is slow and permanent. Like carving in stone. 5-11 trusted authority nodes run on Raspberry Pis in guild members' homes. Cheap. Distributed. Resilient.

## Layer 2 — Delegated Proof of Stake

```javascript
const L2 = {
  consensus: "Delegated Proof of Stake (DPoS)",
  blockTime: "5 seconds",
  throughput: "1000 TPS",
  finality: "fast (2 blocks, ~10 seconds)",
  minStake: "100 GLD",
  checkpointFreq: "every 50 blocks → L1",
  purpose: [
    "ELIZA vetting sessions",
    "PackML state changes",
    "Event bus",
    "SLA timers",
    "Member activity/reputation",
  ],
};

console.log("L2:", L2.consensus);
console.log("TPS:", L2.throughput);
L2.purpose.forEach(p => console.log("  •", p));
```

## The Bridge

The CrossLayerBridge decides what escalates from L2 → L1:

```javascript
const bridge = {
  immediate: ["ethical_refusal", "certification_change", "membership_change", "governance_result"],
  batched:   ["vetting_completion", "audit_summary", "packml_snapshot"],
  never:     ["raw_transcript", "agent_chatter", "temp_state"],
};

console.log("Immediate bridge:", bridge.immediate.join(", "));
console.log("Never on L1:", bridge.never.join(", "));
```

Ethical refusals bypass the checkpoint queue — they go to L1 immediately. Raw transcripts never leave L2.

## Block Structure

Every block has: index, timestamp, previous hash, data hash, layer, validator, nonce. The hash is SHA-256 of all fields concatenated.
