"""
Alarm Tags — alarm status, priority, acknowledgment.
Maps to ISA-18.2 alarm management lifecycle.
"""

import time
from konomi.tags.provider import TagProvider, Tag, TagType


class AlarmTags(TagProvider):
    """Alarm management tags following ISA-18.2."""

    def __init__(self, area: str, unit: str):
        super().__init__(prefix=f"{area}_{unit}")
        self._alarm_count = 0

    def add_alarm(self, name: str, priority: int = 3,
                  setpoint: float = 0.0, deadband: float = 0.0,
                  alarm_type: str = "HI",
                  message: str = "", consequence: str = "",
                  response: str = "") -> dict:
        """
        Add a full ISA-18.2 alarm with all required tags.
        Priority: 1=Emergency, 2=High, 3=Medium, 4=Low.
        """
        tags = {}
        self._alarm_count += 1

        # Active flag
        active = Tag(path=f"ALM_{name}_Active", type=TagType.DISCRETE,
                     desc=f"Alarm {name} active state")
        active.write(False)
        tags["active"] = self.register(active)

        # Acknowledged flag
        acked = Tag(path=f"ALM_{name}_Acked", type=TagType.DISCRETE,
                    desc=f"Alarm {name} acknowledged")
        acked.write(True)
        tags["acked"] = self.register(acked)

        # Priority
        pri = Tag(path=f"ALM_{name}_Priority", type=TagType.INTEGER,
                  desc=f"Alarm {name} priority (1-4)")
        pri.write(priority)
        tags["priority"] = self.register(pri)

        # State (NORMAL/UNACK/ACKED/RTN_UNACK/SHELVED/OOS)
        state = Tag(path=f"ALM_{name}_State", type=TagType.ENUM,
                    desc=f"Alarm {name} state")
        state.write("NORMAL")

        def state_sim():
            if not active.value and acked.value:
                return "NORMAL"
            if active.value and not acked.value:
                return "UNACK"
            if active.value and acked.value:
                return "ACKED"
            if not active.value and not acked.value:
                return "RTN_UNACK"
            return "NORMAL"

        state.set_sim(state_sim)
        tags["state"] = self.register(state)

        # Setpoint
        sp = Tag(path=f"ALM_{name}_SP", type=TagType.ANALOG,
                 desc=f"Alarm {name} setpoint")
        sp.write(setpoint)
        tags["setpoint"] = self.register(sp)

        # Type
        atype = Tag(path=f"ALM_{name}_Type", type=TagType.STRING,
                    desc=f"Alarm {name} type")
        atype.write(alarm_type)
        tags["type"] = self.register(atype)

        # Message
        msg = Tag(path=f"ALM_{name}_Msg", type=TagType.STRING,
                  desc=f"Alarm {name} message")
        msg.write(message or f"{name} {alarm_type} alarm")
        tags["message"] = self.register(msg)

        # Response procedure
        resp = Tag(path=f"ALM_{name}_Response", type=TagType.STRING,
                   desc=f"Alarm {name} operator response")
        resp.write(response)
        tags["response"] = self.register(resp)

        # Consequence
        cons = Tag(path=f"ALM_{name}_Consequence", type=TagType.STRING,
                   desc=f"Alarm {name} consequence of inaction")
        cons.write(consequence)
        tags["consequence"] = self.register(cons)

        return tags

    def add_alarm_summary(self) -> dict:
        """Add area-level alarm summary tags."""
        tags = {}
        for name, desc in [
            ("Total_Active", "Total active alarms"),
            ("Total_Unacked", "Total unacknowledged alarms"),
            ("Highest_Priority", "Highest active alarm priority"),
        ]:
            tag = Tag(path=f"ALM_Summary_{name}",
                      type=TagType.INTEGER, desc=desc)
            tag.write(0)
            tags[name.lower()] = self.register(tag)
        return tags
