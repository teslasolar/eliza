"""
Process Tags — temperatures, pressures, flows, levels.
The analog measurements that make a factory run.
"""

import math
import random
from konomi.tags.provider import TagProvider, Tag, TagType


class ProcessTags(TagProvider):
    """Process measurement tags with sim functions."""

    def __init__(self, area: str, unit: str):
        super().__init__(prefix=f"{area}_{unit}")
        self._tick = 0

    def add_temperature(self, module: str, point: str = "PV",
                        setpoint: float = 72.0, unit: str = "degC",
                        range_lo: float = 0, range_hi: float = 200,
                        desc: str = "") -> Tag:
        """Add a temperature tag with sine-wave sim."""
        tag = Tag(
            path=f"{module}_{point}", type=TagType.ANALOG,
            desc=desc or f"{module} temperature",
            unit=unit, range_lo=range_lo, range_hi=range_hi,
        )
        sp = setpoint

        def sim():
            self._tick += 1
            noise = random.gauss(0, 0.5)
            drift = math.sin(self._tick / 50.0) * 2.0
            return round(sp + drift + noise, 1)

        tag.set_sim(sim)
        return self.register(tag)

    def add_pressure(self, module: str, point: str = "PV",
                     setpoint: float = 14.7, unit: str = "PSI",
                     range_lo: float = 0, range_hi: float = 150,
                     desc: str = "") -> Tag:
        """Add a pressure tag."""
        tag = Tag(
            path=f"{module}_{point}", type=TagType.ANALOG,
            desc=desc or f"{module} pressure",
            unit=unit, range_lo=range_lo, range_hi=range_hi,
        )
        sp = setpoint

        def sim():
            self._tick += 1
            noise = random.gauss(0, 0.2)
            return round(sp + noise, 2)

        tag.set_sim(sim)
        return self.register(tag)

    def add_flow(self, module: str, point: str = "PV",
                 setpoint: float = 100.0, unit: str = "GPM",
                 range_lo: float = 0, range_hi: float = 500,
                 desc: str = "") -> Tag:
        """Add a flow rate tag."""
        tag = Tag(
            path=f"{module}_{point}", type=TagType.ANALOG,
            desc=desc or f"{module} flow rate",
            unit=unit, range_lo=range_lo, range_hi=range_hi,
        )
        sp = setpoint

        def sim():
            self._tick += 1
            noise = random.gauss(0, 1.0)
            ramp = math.sin(self._tick / 100.0) * 5.0
            return round(max(0, sp + ramp + noise), 1)

        tag.set_sim(sim)
        return self.register(tag)

    def add_level(self, module: str, point: str = "PV",
                  setpoint: float = 50.0, unit: str = "pct",
                  range_lo: float = 0, range_hi: float = 100,
                  desc: str = "") -> Tag:
        """Add a tank level tag."""
        tag = Tag(
            path=f"{module}_{point}", type=TagType.ANALOG,
            desc=desc or f"{module} level",
            unit=unit, range_lo=range_lo, range_hi=range_hi,
        )
        sp = setpoint

        def sim():
            self._tick += 1
            noise = random.gauss(0, 0.3)
            saw = ((self._tick % 200) / 200.0) * 10.0 - 5.0
            return round(max(0, min(100, sp + saw + noise)), 1)

        tag.set_sim(sim)
        return self.register(tag)

    def add_setpoint(self, module: str, value: float,
                     unit: str = "", desc: str = "") -> Tag:
        """Add a setpoint tag (writable)."""
        tag = Tag(
            path=f"{module}_SP", type=TagType.ANALOG,
            desc=desc or f"{module} setpoint", unit=unit,
        )
        tag.write(value)
        return self.register(tag)
