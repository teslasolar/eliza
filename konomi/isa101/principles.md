# ISA-101 HMI Design Principles

Foundational guidelines for effective operator displays. Every design decision traces back to these axioms.

```python
class Principles:
    """ISA-101 core design principles expressed as class-level constants.

    Usage::

        if Principles.SITUATIONAL_AWARENESS:
            # always True — awareness trumps aesthetics
            ...
    """

    # --- Priority axioms (left > right) ---
    SITUATIONAL_AWARENESS: str = (
        "Situational awareness takes priority over aesthetics. "
        "Every pixel must earn its place on the display."
    )
    CONSISTENCY: str = (
        "Consistency takes priority over novelty. "
        "Operators must never be surprised by display behaviour."
    )

    # --- Visual foundations ---
    GRAY_BACKGROUND: str = (
        "Use a neutral gray background (approx #808080) to reduce "
        "eye fatigue during 12-hour shifts and preserve colour salience."
    )
    COLOR_IS_MEANING: str = (
        "Colour must encode process meaning — never decoration. "
        "If a colour does not map to a defined state, remove it."
    )

    # --- Information architecture ---
    LAYERS: str = (
        "Organise displays in progressive-detail layers (L1-L5). "
        "Each layer answers a specific question at a specific scope."
    )

    # --- Quick reference dict ---
    ALL: dict = {
        "SITUATIONAL_AWARENESS": SITUATIONAL_AWARENESS,
        "CONSISTENCY": CONSISTENCY,
        "GRAY_BACKGROUND": GRAY_BACKGROUND,
        "COLOR_IS_MEANING": COLOR_IS_MEANING,
        "LAYERS": LAYERS,
    }

    @classmethod
    def summary(cls) -> str:
        """One-line summary for each principle."""
        lines = [f"  {k}: {v.split('.')[0]}." for k, v in cls.ALL.items()]
        return "ISA-101 Principles\n" + "\n".join(lines)
```
