# WebLLM — Running AI Locally in the Browser

## The Problem

Most AI tools send your data to remote servers. For a vetting interview about ethical AI practices, that's... ironic.

## The Solution: WebLLM + WebGPU

WebLLM runs large language models entirely in your browser using WebGPU acceleration. Zero network calls after the initial model download.

```javascript
// How ELIZA loads a model (simplified)
// import * as W from "@mlc-ai/web-llm";
// const engine = await W.CreateMLCEngine("SmolLM2-1.7B-Instruct-q4f16_1-MLC", {
//   initProgressCallback: (p) => console.log(p.text)
// });

// Available models:
const models = {
  "SmolLM2-360M":  { size: "~130MB", quality: "fast, basic" },
  "SmolLM2-1.7B":  { size: "~1GB",   quality: "good balance" },
  "Llama-3.2-1B":  { size: "~700MB", quality: "capable" },
  "Llama-3.2-3B":  { size: "~2GB",   quality: "best, needs GPU" },
};

console.log("Models available:", Object.keys(models).length);
```

## Context Window Management

Small local models have limited context. ELIZA manages this by compressing conversation history:

```javascript
// When context budget is approaching the limit:
// 1. Keep the system prompt (always)
// 2. Summarize completed phases into one message
// 3. Keep the last 2 user+assistant exchanges
// This preserves continuity while staying within budget

const CTX_LIMITS = {
  "SmolLM2-360M":  1500,  // tokens (~6KB)
  "SmolLM2-1.7B":  3000,  // tokens (~12KB)
  "Llama-3.2-3B":  3000,  // tokens (~12KB)
};

console.log("Context limits configured for", Object.keys(CTX_LIMITS).length, "models");
```

## Streaming

ELIZA streams tokens as they're generated — you see the response being "typed" in real time:

```javascript
// Streaming pattern:
// const stream = await engine.chat.completions.create({
//   messages: history,
//   stream: true,
//   max_tokens: 512,
//   temperature: 0.7
// });
// for await (const chunk of stream) {
//   text += chunk.choices[0]?.delta?.content || "";
//   display(text);
// }

console.log("Streaming: token-by-token display");
```

## WebGPU Check

Not all browsers support WebGPU yet. ELIZA checks on load:

```javascript
const hasGPU = typeof navigator !== 'undefined' && !!navigator.gpu;
console.log("WebGPU available:", hasGPU);
```
