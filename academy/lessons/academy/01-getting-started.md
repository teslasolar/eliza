# Getting Started with ACG Academy

## Welcome

The ACG Academy auto-discovers learning modules from the codebase. Every directory with an `academy.md` file becomes a teachable module.

## How Auto-Discovery Works

```javascript
// The academy scans for academy.md in each known directory
const directories = [
  "eliza",       // Vetting interviewer
  "sandbox",     // MCP tool environment
  "konomi",      // Industrial standards
  "guild-chain", // Blockchain
  "scanner",     // Compliance linter
  "academy",     // This module (meta!)
];

console.log("Scanning", directories.length, "directories for academy.md files...");
directories.forEach(d => console.log(`  ${d}/academy.md`));
```

## Creating a Lesson

Lessons are markdown files in `academy/lessons/<module-name>/`:

1. Name them with a number prefix: `01-topic-name.md`
2. Use standard markdown: headings, lists, code blocks
3. JavaScript code blocks can be run live in the browser
4. Python code blocks display as view-only

## Running Code Blocks

Click the "Run Code Blocks" button to execute all JavaScript blocks in a lesson. Results appear in the output bar.

```javascript
// Try it — this block is runnable!
const greeting = "Hello from ACG Academy!";
const timestamp = new Date().toISOString();
console.log(greeting, "at", timestamp);
```

## Structure

```
academy/
  index.html         — Main academy UI
  academy.md         — This module's overview
  lessons/
    eliza/
      01-reverse-turing-test.md
      02-webllm-local-ai.md
      03-vetting-protocol.md
    sandbox/
      01-mcp-tools.md
      02-alignment-scoring.md
    konomi/
      01-self-defining-standards.md
      02-isa88-batch.md
      03-tag-system.md
    guild-chain/
      01-dual-layer-blockchain.md
      02-ethical-refusal.md
      03-3d-vector-blocks.md
    scanner/
      01-compliance-rules.md
    academy/
      01-getting-started.md
```

## Philosophy

Learn by doing. Every lesson is a live document. The code runs. The tools respond. The standards validate. That's the ACG way.
