# ELIZA Academy

The ACG Guild's vetting interviewer — a Reverse Turing Test where AI assesses human alignment.

## What You'll Learn

- How the Reverse Turing Test works and why it matters
- Running AI models locally with WebLLM and WebGPU
- The 6-phase vetting protocol based on the ACG Manifesto
- Building conversational AI interfaces that stream tokens

## Prerequisites

- Modern browser with WebGPU support (Chrome 113+)
- Understanding of the ACG Manifesto's 6 principles
- No server or API keys needed — everything runs locally

## Key Concepts

**Local AI**: ELIZA downloads and runs language models entirely in your browser using WebGPU. No data leaves your device. Models range from 130MB (SmolLM2 360M) to 2GB (Llama 3.2 3B).

**Reverse Turing Test**: Unlike the classic test (can AI fool a human?), ELIZA flips it — can the *human* demonstrate genuine understanding of ethical AI practices?

**6-Phase Protocol**: Each phase maps to one ACG Manifesto principle:
1. Innovation — explore but verify independently
2. Quality — rigorous testing before production
3. Safety & Security — proper harnesses and liability
4. Human Protection — psychological safety first
5. Informed Consent — transparency about AI use
6. Right to Refuse — ethical refusal is professional duty

**Context Management**: Small local models have limited context windows. ELIZA compresses conversation history, summarizing completed phases to stay within budget while maintaining continuity.

## Architecture

- `index.html` — single-file application, no build step
- WebLLM via ESM import from CDN
- Web Speech API for potential voice integration
- Progress tracking with phase pips and seal generation
