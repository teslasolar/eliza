"""python -m konomi.sparkplug — run the Sparkplug B directory."""
import sys
from konomi.serve import run_directory
from konomi.sparkplug.tags import create_provider

sys.exit(run_directory(
    name="sparkplug",
    desc="MQTT/Sparkplug B: topics, payloads, metrics, QoS",
    provides=["MessageType", "SparkplugTopic", "SparkplugPayload",
              "SparkplugMetric", "SparkplugDataType", "QoSLevel"],
    tag_provider=create_provider(),
) or 0)
