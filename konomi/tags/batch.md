# Batch Tags

Batch control process data including phase states, recipe parameters, batch tracking, material charges, and quality checks.

## BatchTags

```python
"""
Batch Tags — batch control process data.
Phase states, recipe parameters, batch tracking.
"""

import time
from konomi.tags.provider import TagProvider, Tag, TagType


class BatchTags(TagProvider):
    """Batch process tags."""

    def __init__(self, area: str, unit: str):
        super().__init__(prefix=f"{area}_{unit}")

    def add_batch_id(self, name: str = "Batch") -> Tag:
        """Current batch ID tag."""
        tag = Tag(path=f"{name}_ID", type=TagType.STRING,
                  desc="Current batch identifier")
        tag.write("")
        return self.register(tag)

    def add_phase_state(self, name: str = "Phase") -> Tag:
        """Current phase state tag (IDLE/RUNNING/COMPLETE/HELD/etc.)."""
        tag = Tag(path=f"{name}_State", type=TagType.ENUM,
                  desc="Current phase state")
        tag.write("IDLE")
        return self.register(tag)

    def add_recipe_param(self, name: str, value: float = 0.0,
                         unit: str = "", desc: str = "") -> Tag:
        """Add a recipe parameter tag."""
        tag = Tag(path=f"Recipe_{name}", type=TagType.ANALOG,
                  desc=desc or f"Recipe param: {name}", unit=unit)
        tag.write(value)
        return self.register(tag)

    def add_step_counter(self, name: str = "Step") -> Tag:
        """Current step number in procedure."""
        tag = Tag(path=f"{name}_Num", type=TagType.INTEGER,
                  desc="Current procedure step number")
        tag.write(0)
        return self.register(tag)

    def add_batch_timer(self, name: str = "Batch") -> Tag:
        """Batch elapsed time in seconds."""
        tag = Tag(path=f"{name}_Timer", type=TagType.ANALOG,
                  desc="Batch elapsed time", unit="s")
        start = [0.0]

        def timer_sim():
            if start[0] == 0:
                return 0.0
            return round(time.time() - start[0], 1)

        tag.set_sim(timer_sim)
        tag._start_ref = start  # keep reference for reset
        return self.register(tag)
```

## Material and Quality Tags

```python
    def add_material_charge(self, material: str, target_kg: float) -> dict:
        """Add material charge tags: target, actual, complete."""
        tags = {}

        target = Tag(path=f"Charge_{material}_Target", type=TagType.ANALOG,
                     desc=f"{material} charge target", unit="kg")
        target.write(target_kg)
        tags["target"] = self.register(target)

        actual = Tag(path=f"Charge_{material}_Actual", type=TagType.ANALOG,
                     desc=f"{material} charge actual", unit="kg")
        actual.write(0.0)
        tags["actual"] = self.register(actual)

        complete = Tag(path=f"Charge_{material}_Done", type=TagType.DISCRETE,
                       desc=f"{material} charge complete")
        complete.set_sim(lambda: (actual.value or 0) >= target_kg * 0.99)
        tags["complete"] = self.register(complete)

        return tags

    def add_quality_check(self, name: str) -> dict:
        """Add quality check tags: value, spec_lo, spec_hi, in_spec."""
        tags = {}

        val = Tag(path=f"QC_{name}_Value", type=TagType.ANALOG,
                  desc=f"QC {name} measured value")
        tags["value"] = self.register(val)

        lo = Tag(path=f"QC_{name}_Lo", type=TagType.ANALOG,
                 desc=f"QC {name} spec low limit")
        tags["spec_lo"] = self.register(lo)

        hi = Tag(path=f"QC_{name}_Hi", type=TagType.ANALOG,
                 desc=f"QC {name} spec high limit")
        tags["spec_hi"] = self.register(hi)

        in_spec = Tag(path=f"QC_{name}_InSpec", type=TagType.DISCRETE,
                      desc=f"QC {name} in-spec flag")

        def spec_sim():
            v = val.value
            lo_v = lo.value
            hi_v = hi.value
            if v is None or lo_v is None or hi_v is None:
                return False
            return lo_v <= v <= hi_v

        in_spec.set_sim(spec_sim)
        tags["in_spec"] = self.register(in_spec)

        return tags
```
