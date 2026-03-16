# Compliance Rules

## What the Scanner Checks

The KONOMI Scanner validates code and configurations against industrial standards and the ACG Manifesto.

## Rule Structure

```javascript
const exampleRule = {
  id: "ISA88-001",
  standard: "ISA-88",
  severity: "error",        // error | warning | info
  pattern: "BatchState",
  check: "Must implement all required PackML states",
  fix: "Add missing states: IDLE, STARTING, EXECUTE, COMPLETING, COMPLETE, STOPPING, STOPPED, ABORTING, ABORTED",
};

console.log("Rule:", exampleRule.id);
console.log("Severity:", exampleRule.severity);
console.log("Check:", exampleRule.check);
```

## Rule Categories

```javascript
const categories = {
  "ISA-88":  ["State machine completeness", "Recipe structure", "Equipment hierarchy"],
  "ISA-95":  ["Enterprise model levels", "Production scheduling", "Material tracking"],
  "ISA-18":  ["Alarm priority distribution", "Shelving policies", "Lifecycle compliance"],
  "ISA-101": ["HMI color standards", "Navigation depth", "Alarm display"],
  "OPC-UA":  ["Node class usage", "Namespace conventions", "Security policy"],
  "Sparkplug": ["Topic structure", "Birth/death certificates", "Metric types"],
  "Modbus":  ["Register alignment", "Function code safety", "Exception handling"],
  "ACG":     ["Transparency disclosure", "AI labeling", "Refusal documentation"],
};

let total = 0;
Object.entries(categories).forEach(([std, rules]) => {
  console.log(`  ${std}: ${rules.length} rule areas`);
  total += rules.length;
});
console.log(`Total: ${total}+ rule areas across ${Object.keys(categories).length} standards`);
```

## Scan Output

The scanner produces structured JSON:

```javascript
const sampleFinding = {
  file: "batch_controller.py",
  line: 42,
  rule_id: "ISA88-001",
  severity: "error",
  message: "Missing PackML states: HOLDING, HELD, RESETTING",
  suggestion: "Add state handlers for HOLDING, HELD, and RESETTING to complete the PackML state model",
};

console.log("Finding:", JSON.stringify(sampleFinding, null, 2));
```

## AI Deep Scan

The AI deep scan goes beyond pattern matching. It uses a local LLM to:
- Understand the *intent* of code, not just its syntax
- Flag subtle non-compliance (e.g., alarm priorities that technically pass but are poorly distributed)
- Suggest architectural improvements based on standard best practices
