# ISA-101 HMI Design

Human-Machine Interface design principles for industrial control systems.

## Key Classes

- **HMIScreen** — A display screen with layout, elements, and navigation
- **HMIElement** — Individual UI element (indicator, button, trend, faceplate)
- **HMINavigation** — Screen hierarchy and navigation model

## Design Axioms

- **Situational Awareness > Aesthetics** — the display must inform, not impress
- **Consistency > Novelty** — same element, same behavior, everywhere
- **Gray background (#808080)** — reduces eye fatigue on 12-hour shifts
- **Color = Meaning** — never use color for decoration; red=alarm, green=running
- **Progressive Detail** — L1 overview → L2 area → L3 unit → L4 loop → L5 diagnostic
