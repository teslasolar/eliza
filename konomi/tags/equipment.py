"""
Equipment Tags — motors, valves, pumps.
Discrete and analog tags for equipment control.
"""

import random
from konomi.tags.provider import TagProvider, Tag, TagType


class EquipmentTags(TagProvider):
    """Equipment control and status tags."""

    def __init__(self, area: str, unit: str):
        super().__init__(prefix=f"{area}_{unit}")

    def add_motor(self, name: str, rated_amps: float = 10.0) -> dict:
        """Add a motor with standard tags: CMD, STS, SPEED, AMPS, FAULT."""
        tags = {}

        cmd = Tag(path=f"{name}_CMD", type=TagType.DISCRETE,
                  desc=f"{name} command (start/stop)")
        cmd.write(False)
        tags["cmd"] = self.register(cmd)

        sts = Tag(path=f"{name}_STS", type=TagType.DISCRETE,
                  desc=f"{name} running status")
        sts.set_sim(lambda: cmd.value)
        tags["sts"] = self.register(sts)

        speed = Tag(path=f"{name}_SPEED", type=TagType.ANALOG,
                    desc=f"{name} speed", unit="RPM",
                    range_lo=0, range_hi=3600)
        ra = rated_amps

        def speed_sim():
            if not cmd.value:
                return 0.0
            return round(1750 + random.gauss(0, 5), 0)

        speed.set_sim(speed_sim)
        tags["speed"] = self.register(speed)

        amps = Tag(path=f"{name}_AMPS", type=TagType.ANALOG,
                   desc=f"{name} current", unit="A",
                   range_lo=0, range_hi=ra * 2)

        def amps_sim():
            if not cmd.value:
                return 0.0
            return round(ra * 0.8 + random.gauss(0, 0.3), 1)

        amps.set_sim(amps_sim)
        tags["amps"] = self.register(amps)

        fault = Tag(path=f"{name}_FLT", type=TagType.DISCRETE,
                    desc=f"{name} fault status")
        fault.set_sim(lambda: random.random() < 0.001)  # rare fault
        tags["fault"] = self.register(fault)

        return tags

    def add_valve(self, name: str) -> dict:
        """Add a valve with CMD, STS, POS tags."""
        tags = {}

        cmd = Tag(path=f"{name}_CMD", type=TagType.DISCRETE,
                  desc=f"{name} command (open/close)")
        cmd.write(False)
        tags["cmd"] = self.register(cmd)

        sts = Tag(path=f"{name}_STS", type=TagType.DISCRETE,
                  desc=f"{name} position status")
        sts.set_sim(lambda: cmd.value)
        tags["sts"] = self.register(sts)

        pos = Tag(path=f"{name}_POS", type=TagType.ANALOG,
                  desc=f"{name} position", unit="pct",
                  range_lo=0, range_hi=100)

        def pos_sim():
            target = 100.0 if cmd.value else 0.0
            current = pos.value or 0.0
            step = (target - current) * 0.3
            return round(current + step, 1)

        pos.set_sim(pos_sim)
        tags["pos"] = self.register(pos)

        return tags

    def add_pump(self, name: str, rated_flow: float = 100.0) -> dict:
        """Add a pump = motor + flow output."""
        tags = self.add_motor(name, rated_amps=15.0)

        flow = Tag(path=f"{name}_FLOW", type=TagType.ANALOG,
                   desc=f"{name} flow rate", unit="GPM",
                   range_lo=0, range_hi=rated_flow * 1.2)
        rf = rated_flow
        cmd = tags["cmd"]

        def flow_sim():
            if not cmd.value:
                return 0.0
            return round(rf * (0.9 + random.gauss(0, 0.02)), 1)

        flow.set_sim(flow_sim)
        tags["flow"] = self.register(flow)

        return tags
