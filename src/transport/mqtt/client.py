import os
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion


def init_client() -> tuple[str, mqtt.Client]:
    cid = _get_client_id()
    host, port = _get_broker_conn()

    client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id=cid)
    client.connect(host=host, port=port)
    return cid, client


def _get_client_id() -> str:
    cid = os.getenv("MQTT_CLIENT_ID")
    if cid is None:
        raise RuntimeError("mqtt client id is not set")

    return cid


def _get_broker_conn() -> tuple[str, int]:
    port = os.getenv("MQTT_PORT", "1883")
    host = os.getenv("MQTT_HOST", "localhost")
    return host, int(port)
