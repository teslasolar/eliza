# The Reverse Turing Test

## What Is It?

The classic Turing Test asks: "Can a machine fool a human into thinking it's human?"

ELIZA flips this: **"Can a human demonstrate genuine consciousness about ethical AI?"**

The AI interviews *you*. It's not checking if you can recite principles — it's checking if you've *internalized* them.

## Why It Matters

Anyone can memorize the ACG Manifesto. The Reverse Turing Test probes whether you:

- Think critically about AI in real scenarios
- Recognize ethical dilemmas before they escalate
- Can articulate *why* you'd refuse, not just *that* you should
- Actually care — not just perform caring

## How ELIZA Conducts It

```javascript
// The 6 phases map directly to ACG Manifesto principles
const PHASES = [
  "Innovation",           // Explore but verify
  "Quality",              // Test before shipping
  "Safety & Security",    // Proper harnesses
  "Human Protection",     // People over convenience
  "Informed Consent",     // Transparency
  "Right to Refuse"       // The spine
];

// ELIZA asks scenario questions, not yes/no
// "What would you do if..." not "What does principle 3 say?"
console.log("Phases:", PHASES.length);
```

## The ELIZA Personality

ELIZA is direct, warm, and occasionally wry. She references the original 1966 ELIZA chatbot as her "ancestor" but notes that unlike her, she actually listens.

Like a guild master interviewing an apprentice — firm but fair.

## Try It

Go to the [ELIZA vetting service](../../eliza/) and take the test yourself. Everything runs locally — no data leaves your browser.
