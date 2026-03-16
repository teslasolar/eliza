# Sparkplug B Compliance Rules

Mandatory behaviors for conformant edge nodes and host applications per the Sparkplug B specification.

## Rule Condition Functions

```python
"""
Sparkplug B Compliance Rules — mandatory behaviors for conformant
edge nodes and host applications per the Sparkplug B specification.
"""

from konomi.meta.rules import Rule, Severity


def _r1_nbirth_first(data: dict) -> bool:
    """Violation: NDATA sent without prior NBIRTH."""
    return (
        data.get("message_type") == "NDATA"
        and not data.get("nbirth_sent", False)
    )


def _r2_seq_increment(data: dict) -> bool:
    """Violation: seq number not incrementing correctly (0-255 wrap)."""
    prev = data.get("prev_seq")
    curr = data.get("curr_seq")
    if prev is None or curr is None:
        return False
    expected = (prev + 1) % 256
    return curr != expected


def _r3_lwt_configured(data: dict) -> bool:
    """Violation: MQTT Last Will and Testament not configured for NDEATH."""
    return (
        data.get("is_edge_node", False)
        and not data.get("lwt_configured", False)
    )


def _r4_alias_optimization(data: dict) -> bool:
    """Violation: metrics not using aliases after NBIRTH for bandwidth."""
    return (
        data.get("message_type") in ("NDATA", "DDATA")
        and data.get("metrics_without_alias", 0) > 0
        and data.get("nbirth_sent", False)
    )


def _r5_store_forward(data: dict) -> bool:
    """Violation: store-and-forward not enabled when disconnected."""
    return (
        data.get("is_disconnected", False)
        and not data.get("store_forward_enabled", False)
    )
```

## Rule Definitions

```python
R1_NBIRTH_BEFORE_NDATA = Rule(
    id="SPARKPLUG-R1",
    condition=_r1_nbirth_first,
    message="NBIRTH must be published before any NDATA or DDATA messages",
    severity=Severity.ERROR,
    fix="Publish NBIRTH with full metric definitions on connect",
    standard="sparkplug",
)

R2_SEQ_INCREMENT = Rule(
    id="SPARKPLUG-R2",
    condition=_r2_seq_increment,
    message="Sequence number must increment 0-255 with wrap-around",
    severity=Severity.ERROR,
    fix="Increment seq by 1 each payload; reset to 0 after 255",
    standard="sparkplug",
)

R3_LWT_NDEATH = Rule(
    id="SPARKPLUG-R3",
    condition=_r3_lwt_configured,
    message="MQTT LWT must be configured to publish NDEATH on disconnect",
    severity=Severity.ERROR,
    fix="Set MQTT Will Topic to NDEATH topic and Will Payload to NDEATH payload",
    standard="sparkplug",
)

R4_ALIAS_BANDWIDTH = Rule(
    id="SPARKPLUG-R4",
    condition=_r4_alias_optimization,
    message="Metric aliases should be used after NBIRTH for bandwidth optimization",
    severity=Severity.WARN,
    fix="Assign numeric aliases in NBIRTH; use aliases in NDATA/DDATA",
    standard="sparkplug",
)

R5_STORE_FORWARD = Rule(
    id="SPARKPLUG-R5",
    condition=_r5_store_forward,
    message="Store-and-forward must be enabled during network disconnection",
    severity=Severity.WARN,
    fix="Buffer metrics locally when MQTT connection is lost; replay on reconnect",
    standard="sparkplug",
)

SPARKPLUG_RULES: list[Rule] = [
    R1_NBIRTH_BEFORE_NDATA,
    R2_SEQ_INCREMENT,
    R3_LWT_NDEATH,
    R4_ALIAS_BANDWIDTH,
    R5_STORE_FORWARD,
]
```
