# Sparkplug B MQTT Tags

Tag provider for MQTT/Sparkplug B. Exposes broker connection, topic counts, sequence tracking, birth/death status, and store-forward state.

```python
"""
Sparkplug Tag Provider — Ignition-style tags for MQTT/Sparkplug B.

Exposes broker connection, topic counts, sequence tracking,
birth/death status, and store-forward state.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class SparkplugTagProvider(TagProvider):
    """Tag provider for Sparkplug B."""

    def __init__(self):
        super().__init__(prefix="SPKPLG")
        self.register(Tag(path="Broker_Connected", type=TagType.DISCRETE,
                          desc="MQTT broker connection status"))
        self.register(Tag(path="Node_Online", type=TagType.DISCRETE,
                          desc="Edge node online (NBIRTH sent)"))
        self.register(Tag(path="Seq_Number", type=TagType.INTEGER,
                          desc="Current sequence number (0-255)"))
        self.register(Tag(path="Device_Count", type=TagType.INTEGER,
                          desc="Registered Sparkplug devices"))
        self.register(Tag(path="Metric_Count", type=TagType.INTEGER,
                          desc="Total metrics across all devices"))
        self.register(Tag(path="Messages_Sent", type=TagType.INTEGER,
                          desc="Total MQTT messages published"))
        self.register(Tag(path="Messages_Queued", type=TagType.INTEGER,
                          desc="Messages in store-forward queue"))
        self.register(Tag(path="QoS_Level", type=TagType.INTEGER,
                          desc="Active QoS level (0/1/2)"))
        self.register(Tag(path="Last_NBIRTH", type=TagType.STRING,
                          desc="Timestamp of last NBIRTH"))
        self.register(Tag(path="Store_Forward", type=TagType.DISCRETE,
                          desc="Store-forward mode active"))
        # Defaults
        self.get("SPKPLG_Broker_Connected").write(False)
        self.get("SPKPLG_Node_Online").write(False)
        self.get("SPKPLG_Seq_Number").write(0)
        self.get("SPKPLG_QoS_Level").write(0)


def create_provider() -> SparkplugTagProvider:
    return SparkplugTagProvider()
```
