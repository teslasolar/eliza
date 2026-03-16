"""
Sparkplug B Topic Namespace — structured MQTT topics for IIoT.
Format: spBv1.0/{group_id}/{message_type}/{edge_node_id}[/{device_id}]
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


SPARKPLUG_NAMESPACE = "spBv1.0"


class MessageType(Enum):
    """Sparkplug B message types."""
    NBIRTH = "NBIRTH"    # Node birth certificate
    NDEATH = "NDEATH"    # Node death certificate
    DBIRTH = "DBIRTH"    # Device birth certificate
    DDEATH = "DDEATH"    # Device death certificate
    NDATA = "NDATA"      # Node data
    DDATA = "DDATA"      # Device data
    NCMD = "NCMD"        # Node command
    DCMD = "DCMD"        # Device command

    @property
    def is_birth(self) -> bool:
        return self in (MessageType.NBIRTH, MessageType.DBIRTH)

    @property
    def is_death(self) -> bool:
        return self in (MessageType.NDEATH, MessageType.DDEATH)

    @property
    def is_node_level(self) -> bool:
        return self in (
            MessageType.NBIRTH, MessageType.NDEATH,
            MessageType.NDATA, MessageType.NCMD,
        )

    @property
    def is_device_level(self) -> bool:
        return self in (
            MessageType.DBIRTH, MessageType.DDEATH,
            MessageType.DDATA, MessageType.DCMD,
        )

    @property
    def requires_device(self) -> bool:
        return self.is_device_level


@dataclass
class SparkplugTopic:
    """A fully-qualified Sparkplug B MQTT topic."""
    group_id: str
    message_type: MessageType
    edge_node_id: str
    device_id: Optional[str] = None

    @property
    def topic(self) -> str:
        """Build the full MQTT topic string."""
        parts = [
            SPARKPLUG_NAMESPACE,
            self.group_id,
            self.message_type.value,
            self.edge_node_id,
        ]
        if self.device_id:
            parts.append(self.device_id)
        return "/".join(parts)

    @classmethod
    def parse(cls, topic_str: str) -> "SparkplugTopic":
        """Parse a topic string into a SparkplugTopic."""
        parts = topic_str.split("/")
        if len(parts) < 4 or parts[0] != SPARKPLUG_NAMESPACE:
            raise ValueError(f"Invalid Sparkplug topic: {topic_str}")
        device_id = parts[4] if len(parts) > 4 else None
        return cls(
            group_id=parts[1],
            message_type=MessageType(parts[2]),
            edge_node_id=parts[3],
            device_id=device_id,
        )

    # Factory methods for each message type
    @classmethod
    def nbirth(cls, group: str, node: str) -> "SparkplugTopic":
        return cls(group, MessageType.NBIRTH, node)

    @classmethod
    def ndeath(cls, group: str, node: str) -> "SparkplugTopic":
        return cls(group, MessageType.NDEATH, node)

    @classmethod
    def dbirth(cls, group: str, node: str, device: str) -> "SparkplugTopic":
        return cls(group, MessageType.DBIRTH, node, device)

    @classmethod
    def ddeath(cls, group: str, node: str, device: str) -> "SparkplugTopic":
        return cls(group, MessageType.DDEATH, node, device)

    @classmethod
    def ndata(cls, group: str, node: str) -> "SparkplugTopic":
        return cls(group, MessageType.NDATA, node)

    @classmethod
    def ddata(cls, group: str, node: str, device: str) -> "SparkplugTopic":
        return cls(group, MessageType.DDATA, node, device)

    @classmethod
    def ncmd(cls, group: str, node: str) -> "SparkplugTopic":
        return cls(group, MessageType.NCMD, node)

    @classmethod
    def dcmd(cls, group: str, node: str, device: str) -> "SparkplugTopic":
        return cls(group, MessageType.DCMD, node, device)

    def __repr__(self):
        return f"SparkplugTopic({self.topic})"

    def __str__(self):
        return self.topic
