# 3D Vector Space Blocks

## The Idea

Standards, code, and knowledge aren't flat. They exist in semantic space with relationships, clusters, and distances. ACG-KCC encodes data into 3D vector coordinates, creating a *spatial blockchain* — an immutable 3D atlas of everything the guild knows.

## Three Axes

```javascript
const axes = {
  x: {
    name: "Domain",
    range: [0, 1000],
    examples: {
      0:   "Meta / Foundational",
      200: "Process Control (ISA-88)",
      400: "Enterprise Integration (ISA-95)",
      600: "Communication (OPC-UA, Sparkplug)",
      800: "Safety & Compliance",
      1000: "Governance & Ethics",
    }
  },
  y: {
    name: "Abstraction",
    range: [0, 1000],
    examples: {
      0:   "Raw data (register values, bits)",
      250: "Tags (named data points)",
      500: "Structures (UDTs, recipes)",
      750: "Standards (ISA-88, ISA-95)",
      1000: "Principles (ACG Manifesto)",
    }
  },
  z: {
    name: "Lifecycle",
    range: [0, 1000],
    examples: {
      0:   "Definition (design time)",
      250: "Configuration (setup)",
      500: "Runtime (production)",
      750: "Monitoring (KPIs, alarms)",
      1000: "Audit (compliance, refusal)",
    }
  },
};

Object.entries(axes).forEach(([axis, info]) => {
  console.log(`${axis.toUpperCase()}-axis: ${info.name} [${info.range.join("-")}]`);
});
```

## Encoding a Standard

Every piece of data gets a 3D coordinate:

```javascript
function encodeToVector(item) {
  // Domain mapping
  const domainMap = {
    meta: 0, base: 50, tags: 100, factory: 150,
    isa88: 200, isa95: 400, isa18: 350, isa101: 300,
    opcua: 600, sparkplug: 650, modbus: 700,
    kpi: 750, scanner: 800, acg: 1000,
  };

  // Abstraction mapping
  const abstractionMap = {
    register: 0, tag: 250, udt: 500, standard: 750, principle: 1000,
  };

  // Lifecycle mapping
  const lifecycleMap = {
    define: 0, configure: 250, runtime: 500, monitor: 750, audit: 1000,
  };

  return {
    x: domainMap[item.domain] || 500,
    y: abstractionMap[item.abstraction] || 500,
    z: lifecycleMap[item.lifecycle] || 500,
  };
}

// Examples
const vectors = [
  { name: "ISA-88 Batch State Machine",  ...encodeToVector({domain:"isa88", abstraction:"standard", lifecycle:"runtime"}) },
  { name: "Temperature Tag",             ...encodeToVector({domain:"tags", abstraction:"tag", lifecycle:"runtime"}) },
  { name: "ACG Principle 6 (Refuse)",    ...encodeToVector({domain:"acg", abstraction:"principle", lifecycle:"audit"}) },
  { name: "Modbus Register Map",         ...encodeToVector({domain:"modbus", abstraction:"register", lifecycle:"configure"}) },
  { name: "OPC-UA Node Definition",      ...encodeToVector({domain:"opcua", abstraction:"udt", lifecycle:"define"}) },
];

vectors.forEach(v => console.log(`  [${v.x}, ${v.y}, ${v.z}] ${v.name}`));
```

## Vector Block

A vector block extends the standard block with 3D coordinates:

```javascript
function createVectorBlock(index, prevHash, data, vector) {
  const block = {
    index,
    timestamp: Date.now() / 1000,
    prev_hash: prevHash,
    data,
    vector: { x: vector.x, y: vector.y, z: vector.z },
    magnitude: Math.sqrt(vector.x**2 + vector.y**2 + vector.z**2),
  };

  // Hash includes vector coordinates
  const raw = `${block.index}${block.timestamp}${block.prev_hash}` +
              `${JSON.stringify(block.data)}${block.vector.x}${block.vector.y}${block.vector.z}`;

  // Simple hash for demo (real impl uses SHA-256)
  let h = 0;
  for (let i = 0; i < raw.length; i++) h = ((h << 5) - h + raw.charCodeAt(i)) | 0;
  block.hash = Math.abs(h).toString(16).padStart(8, "0");

  return block;
}

const genesis = createVectorBlock(0, "0".repeat(64),
  { type: "genesis", message: "ACG-KCC Vector Genesis" },
  { x: 500, y: 500, z: 500 }
);
console.log("Genesis block:", JSON.stringify(genesis, null, 2));
```

## Spatial Queries

With 3D coordinates, you can query the blockchain spatially:

- "Show me everything in the ISA-88 domain" → filter x: 180-220
- "What's at the principle level?" → filter y: 900-1000
- "What's in audit phase?" → filter z: 900-1000
- "What's near this standard?" → euclidean distance from target vector

## Why It Matters

Flat blockchains store data in sequence. Vector blockchains store data in *space*. Similar concepts cluster together. You can find related standards by proximity, not just by searching text.
