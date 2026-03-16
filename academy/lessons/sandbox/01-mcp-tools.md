# MCP Tools — Model Context Protocol

## What Is MCP?

MCP (Model Context Protocol) is a standardized way for AI models to call external tools. Instead of the model trying to do everything with text, it can request structured tool calls.

## Anatomy of a Tool

Every MCP tool has:

```javascript
const toolSchema = {
  name: "acg_lookup_principle",
  description: "Look up ACG Manifesto principles by number",
  parameters: {
    number: {
      type: "string",
      description: "Principle number (1-6) or 'all'"
    }
  }
};

console.log("Tool:", toolSchema.name);
console.log("Params:", Object.keys(toolSchema.parameters).join(", "));
```

## The Sandbox Tool Registry

The sandbox provides 6 tools:

```javascript
const tools = [
  "acg_lookup_principle    — Look up manifesto principles",
  "acg_check_alignment     — Score text against principles",
  "acg_generate_scenario   — Generate vetting scenarios",
  "acg_hash_response       — Hash vetting responses",
  "konomi_query            — Search konomi packages",
  "konomi_factory_status   — Factory tag status",
];

tools.forEach((t, i) => console.log(`  ${i+1}. ${t}`));
```

## Transport Layers

The same tools are served three ways:

- **REST API** (`server.py`) — HTTP endpoints on port 8066
- **MCP stdio** (`mcp_stdio.py`) — JSON-RPC over stdin/stdout
- **Browser** (`voice.html`, `index.html`) — client-side JavaScript

## Building a New Tool

1. Define the function in `tools.py`
2. Register it in `registry.py` with schema
3. It's automatically available on all transports

The registry validates parameters against the schema before calling the tool function.
