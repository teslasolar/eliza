# ACG Guild Platform — Automated Tools

**AI Craftspeople Guild · Local-first tools for ethical AI engineering**

## Tools

| Tool | Description | Path |
|------|-------------|------|
| **ELIZA** | Reverse Turing Test — vetting interview against the 6 ACG principles | [`/index.html`](index.html) |
| **KONOMI Scanner** | Standards compliance scanner — linter on steroids for ISA/ACG standards | [`/scanner/`](scanner/) |

All tools run **100% locally** via WebLLM + WebGPU. Zero backend. Zero API keys. Zero data transmitted.

---

# ELIZA — ACG Automated Vetting Service

**The Reverse Turing Test — Is the human conscious? And if so, are they enjoying it?**

ELIZA is the AI Craftspeople Guild's automated vetting interview tool. Named after the 1966 ELIZA chatbot — but unlike the original, this one actually listens.

A local AI interviews you against the six principles of the [ACG Manifesto](https://aicraftspeopleguild.github.io/aicraftspeopleguild-manifesto.html). Pass all six phases, earn the **⚒ Vetted by ACG** seal. The vetting is a conversation, not a quiz — ELIZA asks scenario questions to assess whether you genuinely think about ethical AI practice.

## The Six Phases

1. **Embracing Innovation** — Do you adopt AI thoughtfully or chase hype?
2. **Demanding Quality** — Do you verify AI outputs before shipping?
3. **Ensuring Safety & Security** — Do you think about threat models?
4. **Protecting Humans** — Do you prioritize human wellbeing over metrics?
5. **Respecting User Agency** — Do you insist on transparency?
6. **Right and Duty to Refuse** — Will you say no when it matters?

## How to Use

1. Open `index.html` in a WebGPU-capable browser (Chrome 113+, Edge 113+)
2. Select an AI model from the dropdown
3. Click **⚒ Begin Vetting**
4. The model downloads to your device on first use (cached after that)
5. ELIZA interviews you through all six phases
6. Receive your result — **Vetted by ACG** or feedback on areas for growth

## Available Models

| Model | Size | Notes |
|-------|------|-------|
| SmolLM2 360M | ~130MB | Fast download, quick responses |
| SmolLM2 1.7B | ~1GB | Better conversational quality |
| Llama 3.2 1B | ~700MB | Good balance of quality and speed |
| Llama 3.2 3B | ~2GB | Best quality, requires decent GPU |

## Privacy

ELIZA runs **100% locally** on your device. This is not a feature — it's the point.

- Zero API calls (no Anthropic, no OpenAI, nothing)
- Zero analytics or tracking
- Zero cookies (only browser Cache Storage for the model)
- All inference via WebGPU on your GPU
- Conversation lives in memory, gone on page close

An AI vetting tool that phones home would violate the very charter it assesses against.

## Local Development

```bash
python3 -m http.server 8080
# Open http://localhost:8080 in Chrome 113+
```

## Browser Requirements

- **Supported:** Chrome 113+, Edge 113+, Firefox Nightly (with WebGPU flag)
- **Not yet supported:** Safari (no WebGPU), older browsers

## Architecture

- Single HTML file, all CSS/JS inline
- Zero build step, zero dependencies, zero framework
- [WebLLM](https://github.com/mlc-ai/web-llm) via CDN for on-device inference
- Vanilla JS with ES modules

---

# KONOMI Scanner — Standards Compliance

**Linter on steroids — inspect and verify whether your solutions meet the bar**

The KONOMI Scanner checks code against industrial standards (ISA-95, ISA-88, ISA-101, ISA-18.2, OPC-UA, Sparkplug, Modbus) and the ACG Manifesto principles.

### Two Scan Modes

- **Static Scan** — Instant pattern-matching rules. No GPU needed. Works in any browser.
- **Deep Scan** — Static rules + AI-powered semantic analysis via WebLLM. Catches architectural issues that regex can't.

### What It Checks

| Standard | What's Checked |
|----------|---------------|
| ISA-88 | State machine patterns, recipe hierarchy, hardcoded states |
| ISA-95 | Equipment hierarchy, data flow level crossing |
| ISA-18.2 | Alarm priority, alarm states, actionable responses |
| ISA-101 | Hardcoded UI values, HMI layer hierarchy |
| OPC-UA | Direct device addressing vs. node paths |
| Sparkplug | NBIRTH ordering, LWT configuration |
| Modbus | Byte order specification for multi-register values |
| ACG | AI output verification, input validation, AI disclosure, error handling, PII logging |

### Severity Levels

- **Fatal/Error** — Must fix. Standards violation that will cause problems.
- **Warning** — Should fix. Missing best practice or incomplete implementation.
- **Info** — Consider. Architectural suggestion or optimization opportunity.

---

## Credits

ACG Manifesto by Alex Bunardzic, Woody Zuill, Jona Heidsick, Matt Burch, Alex Thurow, Tsvetan Tsvetanov.

Konomi Standard spec by Thomas (ThomasTheTankEngineer).

⚒ ACG
