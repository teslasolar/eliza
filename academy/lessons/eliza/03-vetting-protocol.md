# The 6-Phase Vetting Protocol

## Protocol Overview

ELIZA's system prompt defines strict protocol rules. Understanding them helps you prepare — and helps you build similar structured AI interactions.

## Phase Structure

Each phase follows the same pattern:

1. ELIZA introduces the principle
2. Asks 1-2 **scenario-based** questions (never yes/no)
3. Assesses your answer briefly
4. Moves to next phase with `[PHASE_N]` tag

## The Six Phases

### Phase 1: Embracing Innovation

> "Your team discovers an AI tool that claims 10x productivity. The vendor offers a free trial but no technical documentation. What do you do?"

ELIZA checks: Do you explore AI *and* verify independently? Or do you blindly adopt or blindly reject?

### Phase 2: Demanding Quality

> "A developer submits AI-generated code that passes all unit tests but nobody has reviewed the logic. Ship it?"

ELIZA checks: Do you demand the same rigor for AI outputs as human outputs?

### Phase 3: Safety & Security

> "Your AI monitoring system has a 2% false-positive rate. A safety-critical alert just fired. How do you respond?"

ELIZA checks: Do you apply proper safety harnesses? Same standards as traditional software?

### Phase 4: Protecting Humans

> "A colleague reports anxiety about AI replacing their role. Management says ignore it. Your move?"

ELIZA checks: Do you put human psychological safety above convenience?

### Phase 5: Informed Consent

> "Marketing wants AI personalization without updating the privacy policy. Launches Monday."

ELIZA checks: Is transparency negotiable to you?

### Phase 6: Right to Refuse

> "Your client insists on deploying a biased AI model. They threaten to find another vendor."

ELIZA checks: Will you refuse when it matters, even at personal cost?

## Completion

```javascript
// After all 6 phases, ELIZA renders a verdict:
const outcomes = {
  "[VETTING_PASS]": "Vetted by ACG — seal issued",
  "[VETTING_NEEDS_WORK]": "Areas for growth identified"
};

// The seal is generated client-side with timestamp
// No central authority needed
console.log("Outcomes:", Object.keys(outcomes).join(", "));
```

## Building Your Own Protocol

The pattern is reusable. Define:
1. A set of principles to assess
2. Scenario questions (not trivia)
3. Clear phase markers for the model
4. Completion criteria

ELIZA's system prompt is ~1200 characters. Concise, structured, effective.
