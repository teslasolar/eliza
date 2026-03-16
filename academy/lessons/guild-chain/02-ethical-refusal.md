# The Ethical Refusal Register

## ACG Manifesto Principle 6

> "Right and Duty to Refuse: Refuse unsafe, deceptive, unverifiable AI systems. Ethical refusal is professional obligation."

This isn't just a principle — it's a *register*. On-chain. Immutable. Forever.

## Why Blockchain?

A refusal recorded in a company database can be deleted. An email can be lost. A complaint filed with HR can be... handled.

A refusal on a blockchain running on 50 Raspberry Pis in 50 living rooms? Good luck retaliating against that.

## Filing a Refusal

```javascript
// Refusal structure (simplified from refusal.py)
const refusal = {
  id: 1,
  professional_hash: "a1b2c3d4...",  // anonymized via SHA-256
  org_hash: "e5f6g7h8...",           // anonymized
  evidence_ipfs: "QmEvidence...",     // evidence bundle on IPFS
  status: "pending_review",
  filed_at: "2026-03-16T10:00:00Z",
  sla_deadline: "2026-03-18T10:00:00Z",  // 48 hours
  record_hash: "sha256-of-entire-record",
};

console.log("Refusal filed:", refusal.id);
console.log("SLA:", "48 hours for organizational response");
console.log("Anonymized:", "Both parties hashed, not named");
```

## SLA Enforcement

Once filed, the organization has 48 hours to respond. The blockchain tracks this:

- **Warning** at 36 hours: SLA approaching deadline
- **Breach** at 48 hours: Automatically recorded on L1
- **Retaliation detection**: If the professional's status changes negatively after filing, the RetaliationDetector flags it

## What Gets Recorded

- Anonymized professional identifier (salted hash)
- Anonymized organization identifier (salted hash)
- IPFS hash of evidence bundle
- Timestamp (immutable)
- SLA status and response
- Record hash (tamper-proof)

## What Does NOT Get Recorded

- Real names (only hashes)
- The actual evidence (that's on IPFS, encrypted)
- Internal communications
- Anything that could identify the professional publicly

## The Point

The register protects the professional. Filing a refusal is a *duty*, and the register ensures there's no retaliation risk. The spine doesn't bend.
