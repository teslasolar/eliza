# ISA-18.2 Alarm States and Lifecycle State Machine

States: NORMAL, UNACK, ACKED, RTN_UNACK, SHELVED, OUT_OF_SERVICE. The state machine encodes every valid transition per ISA-18.2.

## AlarmState Dataclass

```python
from dataclasses import dataclass
from konomi.meta.state_machine import StateMachine


@dataclass
class AlarmState:
    """Snapshot of an alarm's lifecycle state flags."""
    name: str
    active: bool = False
    acknowledged: bool = True
    suppressed: bool = False
    out_of_service: bool = False
    desc: str = ""

    @property
    def needs_attention(self) -> bool:
        """True when operator action is required."""
        return self.active and not self.acknowledged

    @property
    def is_clear(self) -> bool:
        """True when alarm is fully resolved and acknowledged."""
        return not self.active and self.acknowledged and not self.suppressed

    def describe(self) -> dict:
        return {
            "name": self.name,
            "active": self.active,
            "acknowledged": self.acknowledged,
            "suppressed": self.suppressed,
            "out_of_service": self.out_of_service,
        }

    def __repr__(self):
        return f"AlarmState({self.name})"
```

## Canonical Alarm State Definitions

```python
ALARM_STATES: dict[str, AlarmState] = {
    "NORMAL": AlarmState(
        name="NORMAL",
        active=False, acknowledged=True, suppressed=False,
        desc="Process within limits, no alarm active",
    ),
    "UNACK": AlarmState(
        name="UNACK",
        active=True, acknowledged=False, suppressed=False,
        desc="Alarm active and not yet acknowledged — needs attention",
    ),
    "ACKED": AlarmState(
        name="ACKED",
        active=True, acknowledged=True, suppressed=False,
        desc="Alarm active, operator aware, condition still present",
    ),
    "RTN_UNACK": AlarmState(
        name="RTN_UNACK",
        active=False, acknowledged=False, suppressed=False,
        desc="Alarm condition cleared but not yet acknowledged",
    ),
    "SHELVED": AlarmState(
        name="SHELVED",
        active=False, acknowledged=True, suppressed=True,
        desc="Alarm temporarily suppressed by operator with time limit",
    ),
    "OUT_OF_SERVICE": AlarmState(
        name="OUT_OF_SERVICE",
        active=False, acknowledged=True, suppressed=True,
        out_of_service=True,
        desc="Alarm disabled — maintenance or commissioning",
    ),
}
```

## Alarm Lifecycle State Machine

```python
def create_alarm_state_machine(name: str = "AlarmLifecycle") -> StateMachine:
    """Build the ISA-18.2 alarm lifecycle state machine.

    Key paths::

        NORMAL -> UNACK          (alarm trips)
        UNACK  -> ACKED          (operator acknowledges)
        ACKED  -> NORMAL         (condition clears)
        UNACK  -> RTN_UNACK      (condition clears before ack)
        RTN_UNACK -> NORMAL      (operator acknowledges)
        NORMAL -> SHELVED        (operator shelves)
        SHELVED -> NORMAL        (shelf timer expires or unshelve)
        NORMAL -> OUT_OF_SERVICE (maintenance disables)
        OUT_OF_SERVICE -> NORMAL (maintenance re-enables)
    """
    sm = StateMachine(name=name, initial="NORMAL")
    for s in ALARM_STATES:
        sm.add_state(s)

    # --- Alarm trip / clear cycle ---
    sm.add_transition("NORMAL", "UNACK", "trip",
                       desc="Process crosses alarm setpoint")
    sm.add_transition("UNACK", "ACKED", "acknowledge",
                       desc="Operator acknowledges active alarm")
    sm.add_transition("ACKED", "NORMAL", "clear",
                       desc="Process returns within limits")
    sm.add_transition("UNACK", "RTN_UNACK", "clear",
                       desc="Process clears before operator ack")
    sm.add_transition("RTN_UNACK", "NORMAL", "acknowledge",
                       desc="Operator acks a returned alarm")

    # --- Re-trip from acknowledged ---
    sm.add_transition("ACKED", "UNACK", "trip",
                       desc="Condition re-trips after brief clear")

    # --- Shelving ---
    sm.add_transition("NORMAL", "SHELVED", "shelve",
                       desc="Operator temporarily suppresses alarm")
    sm.add_transition("SHELVED", "NORMAL", "unshelve",
                       desc="Shelf timer expires or operator unshelves")

    # --- Out of service ---
    sm.add_transition("NORMAL", "OUT_OF_SERVICE", "disable",
                       desc="Maintenance takes alarm out of service")
    sm.add_transition("OUT_OF_SERVICE", "NORMAL", "enable",
                       desc="Maintenance returns alarm to service")

    return sm
```
