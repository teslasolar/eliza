"""
ISA-88 State Machines — Phase, Batch, and PackML/Unit state models.

Builds on konomi.meta.state_machine.StateMachine with factory functions
that return fully configured instances per the ISA-88 standard.
"""

from konomi.meta.state_machine import StateMachine


# ---------------------------------------------------------------------------
# Phase State Machine  (ISA-88 procedural state model)
# ---------------------------------------------------------------------------
# States: IDLE, RUNNING, COMPLETE, HOLDING, HELD, RESTARTING,
#         STOPPING, STOPPED, ABORTING, ABORTED
# ---------------------------------------------------------------------------

def create_phase_state_machine(name: str = "PhaseState") -> StateMachine:
    """Create an ISA-88 phase state machine.

    Transitions:
        IDLE -> RUNNING -> COMPLETE
        RUNNING -> HOLDING -> HELD -> RESTARTING -> RUNNING
        RUNNING -> STOPPING -> STOPPED
        RUNNING -> ABORTING -> ABORTED
        IDLE -> ABORTING  (abort from idle)
    """
    sm = StateMachine(name=name, initial="IDLE")
    for s in [
        "IDLE", "RUNNING", "COMPLETE",
        "HOLDING", "HELD", "RESTARTING",
        "STOPPING", "STOPPED",
        "ABORTING", "ABORTED",
    ]:
        sm.add_state(s)

    # Normal path
    sm.add_transition("IDLE", "RUNNING", "start")
    sm.add_transition("RUNNING", "COMPLETE", "complete")

    # Hold path
    sm.add_transition("RUNNING", "HOLDING", "hold")
    sm.add_transition("HOLDING", "HELD", "held")
    sm.add_transition("HELD", "RESTARTING", "restart")
    sm.add_transition("RESTARTING", "RUNNING", "running")

    # Stop path
    sm.add_transition("RUNNING", "STOPPING", "stop")
    sm.add_transition("HOLDING", "STOPPING", "stop")
    sm.add_transition("HELD", "STOPPING", "stop")
    sm.add_transition("RESTARTING", "STOPPING", "stop")
    sm.add_transition("STOPPING", "STOPPED", "stopped")

    # Abort path (from any active state)
    for src in ["IDLE", "RUNNING", "HOLDING", "HELD",
                "RESTARTING", "STOPPING", "STOPPED"]:
        sm.add_transition(src, "ABORTING", "abort")
    sm.add_transition("ABORTING", "ABORTED", "aborted")

    return sm


# ---------------------------------------------------------------------------
# Batch State Machine  (ISA-88 batch lifecycle)
# ---------------------------------------------------------------------------
# States: CREATED, SCHEDULED, RUNNING, COMPLETE, HELD, ABORTED
# ---------------------------------------------------------------------------

def create_batch_state_machine(name: str = "BatchState") -> StateMachine:
    """Create an ISA-88 batch lifecycle state machine.

    Transitions:
        CREATED -> SCHEDULED -> RUNNING -> COMPLETE
        RUNNING -> HELD -> RUNNING
        RUNNING -> ABORTED
    """
    sm = StateMachine(name=name, initial="CREATED")
    for s in ["CREATED", "SCHEDULED", "RUNNING", "COMPLETE",
              "HELD", "ABORTED"]:
        sm.add_state(s)

    sm.add_transition("CREATED", "SCHEDULED", "schedule")
    sm.add_transition("SCHEDULED", "RUNNING", "start")
    sm.add_transition("RUNNING", "COMPLETE", "complete")
    sm.add_transition("RUNNING", "HELD", "hold")
    sm.add_transition("HELD", "RUNNING", "restart")
    sm.add_transition("RUNNING", "ABORTED", "abort")
    sm.add_transition("HELD", "ABORTED", "abort")

    return sm


# ---------------------------------------------------------------------------
# PackML / Unit State Machine  (ISA-88 / ISA-TR88)
# ---------------------------------------------------------------------------
# States: STOPPED, IDLE, STARTING, EXECUTE, COMPLETING, COMPLETE,
#         RESETTING, HOLDING, HELD, UNHOLDING,
#         SUSPENDING, SUSPENDED, UNSUSPENDING,
#         ABORTING, ABORTED, CLEARING,
#         STOPPING
# ---------------------------------------------------------------------------

_PACKML_STATES = [
    "STOPPED", "IDLE", "STARTING", "EXECUTE",
    "COMPLETING", "COMPLETE", "RESETTING",
    "HOLDING", "HELD", "UNHOLDING",
    "SUSPENDING", "SUSPENDED", "UNSUSPENDING",
    "ABORTING", "ABORTED", "CLEARING",
    "STOPPING",
]

# States from which STOPPING is allowed (all except STOPPED/ABORTING/ABORTED)
_STOPPABLE = [
    "IDLE", "STARTING", "EXECUTE", "COMPLETING", "COMPLETE",
    "RESETTING", "HOLDING", "HELD", "UNHOLDING",
    "SUSPENDING", "SUSPENDED", "UNSUSPENDING",
    "CLEARING",
]

# States from which ABORTING is allowed (all except ABORTING/ABORTED)
_ABORTABLE = _STOPPABLE + ["STOPPED", "STOPPING"]


def create_unit_state_machine(name: str = "UnitState") -> StateMachine:
    """Create a PackML / ISA-88 unit state machine.

    Key paths:
        STOPPED <-> IDLE -> STARTING -> EXECUTE -> COMPLETING -> COMPLETE
        COMPLETE -> RESETTING -> IDLE
        EXECUTE -> HOLDING -> HELD -> UNHOLDING -> EXECUTE
        EXECUTE -> SUSPENDING -> SUSPENDED -> UNSUSPENDING -> EXECUTE
        any -> STOPPING -> STOPPED
        any -> ABORTING -> ABORTED -> CLEARING -> STOPPED
    """
    sm = StateMachine(name=name, initial="STOPPED")
    for s in _PACKML_STATES:
        sm.add_state(s)

    # Normal cycle
    sm.add_transition("STOPPED", "RESETTING", "reset")
    sm.add_transition("RESETTING", "IDLE", "idle")
    sm.add_transition("IDLE", "STARTING", "start")
    sm.add_transition("STARTING", "EXECUTE", "sc")  # state complete
    sm.add_transition("EXECUTE", "COMPLETING", "complete")
    sm.add_transition("COMPLETING", "COMPLETE", "sc")
    sm.add_transition("COMPLETE", "RESETTING", "reset")

    # Hold path
    sm.add_transition("EXECUTE", "HOLDING", "hold")
    sm.add_transition("HOLDING", "HELD", "sc")
    sm.add_transition("HELD", "UNHOLDING", "unhold")
    sm.add_transition("UNHOLDING", "EXECUTE", "sc")

    # Suspend path
    sm.add_transition("EXECUTE", "SUSPENDING", "suspend")
    sm.add_transition("SUSPENDING", "SUSPENDED", "sc")
    sm.add_transition("SUSPENDED", "UNSUSPENDING", "unsuspend")
    sm.add_transition("UNSUSPENDING", "EXECUTE", "sc")

    # Stop from any stoppable state
    for src in _STOPPABLE:
        sm.add_transition(src, "STOPPING", "stop")
    sm.add_transition("STOPPING", "STOPPED", "sc")

    # Abort from any abortable state
    for src in _ABORTABLE:
        sm.add_transition(src, "ABORTING", "abort")
    sm.add_transition("ABORTING", "ABORTED", "sc")
    sm.add_transition("ABORTED", "CLEARING", "clear")
    sm.add_transition("CLEARING", "STOPPED", "sc")

    return sm
