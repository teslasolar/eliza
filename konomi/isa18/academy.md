# ISA-18.2 Alarm Management

Alarm lifecycle, priorities, shelving, and rationalization for industrial systems.

## Key Classes

- **Alarm** — An alarm instance with state, priority, and timestamp
- **AlarmPriority** — Critical, High, Medium, Low, Diagnostic
- **AlarmState** — Normal, Active, Acknowledged, Suppressed, Shelved
- **AlarmShelving** — Temporary alarm suppression with expiry

## Core Concepts

- **Alarm Lifecycle**: NORMAL → ACTIVE → ACKNOWLEDGED → RETURN_TO_NORMAL
- **Priority Distribution**: Most alarms should be Low/Medium; too many Critical alarms means poor rationalization
- **Shelving**: Temporary suppression during maintenance — must auto-expire
- **Alarm Flooding**: >10 alarms/10min per operator = flood condition
