# Sparkplug B / MQTT

Lightweight publish/subscribe messaging for industrial IoT — topics, payloads, metrics, and QoS.

## Key Classes

- **MessageType** — NBIRTH, NDATA, NDEATH, DBIRTH, DDATA, DDEATH
- **SparkplugTopic** — Structured topic: spBv1.0/group/msgtype/edge/device
- **SparkplugPayload** — Protobuf payload with metrics and timestamp
- **SparkplugMetric** — Named metric with type, value, and alias
- **SparkplugDataType** — Int8 through String, DateTime, DataSet
- **QoSLevel** — 0 (at most once), 1 (at least once)

## Core Concepts

- **Birth/Death Certificates**: Devices announce themselves (NBIRTH) and the broker detects disconnection (NDEATH)
- **Topic Namespace**: `spBv1.0/{group}/{msgtype}/{edge_node}/{device}`
- **Metric Aliases**: First BIRTH sends full names; subsequent DATA sends use numeric aliases for efficiency
- **State Awareness**: Unlike raw MQTT, Sparkplug guarantees you always know current state
