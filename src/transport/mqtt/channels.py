import paho.mqtt.client as mqtt
from .codec import Codec
from dataclasses import asdict
import transport.protocols as p
import common.entities as e


TICK_TOPIC = "lab/tick"
SIGNAL_TOPIC = "lab/signal"
HEARTBEAT_TOPIC = "lab/heartbeat"
TRACK_SAMPLE_TOPIC = "lab/track"
STATION_REPORT_TOPIC = "lab/station_report"
LOCALIZED_SAMPLE_TOPIC = "lab/localized_sample"


class HeartbeatChannel:
    def __init__(self, client_id: str, client: mqtt.Client, codec: Codec):
        self._id = client_id
        self._client = client
        self._codec = codec

    def subscribe(self, handler: p.HeartbeatHandler):
        def callback(client, userdata, message: mqtt.MQTTMessage) -> None:
            d = self._codec.unmarshal(message.payload)
            heartbeat = e.Heartbeat.from_dict(d)
            handler(heartbeat)

        topic = HEARTBEAT_TOPIC + "/#"
        self._client.subscribe(topic)
        self._client.message_callback_add(topic, callback)

    def publish(self, hb: e.Heartbeat) -> None:
        raw = self._codec.marshal(asdict(hb))
        topic = HEARTBEAT_TOPIC + f"/{self._id}"
        self._client.publish(topic, raw)


class LocalizedSampleChannel:
    def __init__(self, client_id: str, client: mqtt.Client, codec: Codec):
        self._id = client_id
        self._client = client
        self._codec = codec

    def subscribe(self, handler: p.LocalizedSampleHandler):
        def callback(client, userdata, message: mqtt.MQTTMessage) -> None:
            d = self._codec.unmarshal(message.payload)
            sample = e.LocalizedSample.from_dict(d)
            handler(sample)

        topic = LOCALIZED_SAMPLE_TOPIC + "/#"
        self._client.subscribe(topic)
        self._client.message_callback_add(topic, callback)

    def publish(self, sample: e.LocalizedSample) -> None:
        raw = self._codec.marshal(asdict(sample))
        topic = LOCALIZED_SAMPLE_TOPIC + f"/{self._id}"
        self._client.publish(topic, raw)


class SignalChannel:
    def __init__(self, client_id: str, client: mqtt.Client, codec: Codec):
        self._id = client_id
        self._client = client
        self._codec = codec
        self._handlers: list[p.SignalHandler] = []

    def subscribe(self, handler: p.SignalHandler):
        if self._handlers:
            self._handlers.append(handler)
            return

        def callback(client, userdata, message: mqtt.MQTTMessage) -> None:
            d = self._codec.unmarshal(message.payload)
            signal = e.Signal.from_dict(d)
            for handler in self._handlers:
                handler(signal)

        topic = SIGNAL_TOPIC + "/#"
        self._client.subscribe(topic)
        self._client.message_callback_add(topic, callback)
        self._handlers.append(handler)

    def publish(self, signal: e.Signal) -> None:
        raw = self._codec.marshal(asdict(signal))
        topic = SIGNAL_TOPIC + f"/{self._id}"
        self._client.publish(topic, raw)


class StationReportChannel:
    def __init__(self, client_id: str, client: mqtt.Client, codec: Codec):
        self._id = client_id
        self._client = client
        self._codec = codec

    def subscribe(self, handler: p.StationReportHandler):
        def callback(client, userdata, message: mqtt.MQTTMessage) -> None:
            d = self._codec.unmarshal(message.payload)
            report = e.StationReport.from_dict(d)
            handler(report)

        topic = STATION_REPORT_TOPIC + "/#"
        self._client.subscribe(topic)
        self._client.message_callback_add(topic, callback)

    def publish(self, report: e.StationReport) -> None:
        raw = self._codec.marshal(asdict(report))
        topic = STATION_REPORT_TOPIC + f"/{self._id}"
        self._client.publish(topic, raw)


class TickChannel:
    def __init__(self, client_id: str, client: mqtt.Client, codec: Codec):
        self._id = client_id
        self._client = client
        self._codec = codec
        self._handlers: list[p.TickHandler] = []

    def subscribe(self, handler: p.TickHandler):
        if self._handlers:
            self._handlers.append(handler)
            return

        def callback(client, userdata, message: mqtt.MQTTMessage) -> None:
            d = self._codec.unmarshal(message.payload)
            tick = e.Tick(**d)
            for handler in self._handlers:
                handler(tick)

        topic = TICK_TOPIC + "/#"
        self._client.subscribe(topic)
        self._client.message_callback_add(topic, callback)
        self._handlers.append(handler)

    def publish(self, tick: e.Tick) -> None:
        raw = self._codec.marshal(asdict(tick))
        topic = TICK_TOPIC + f"/{self._id}"
        self._client.publish(topic, raw)


class TrackSampleChannel:
    def __init__(self, client_id: str, client: mqtt.Client, codec: Codec):
        self._id = client_id
        self._client = client
        self._codec = codec

    def subscribe(self, handler: p.TrackSampleHandler):
        def callback(client, userdata, message: mqtt.MQTTMessage) -> None:
            d = self._codec.unmarshal(message.payload)
            sample = e.TrackSample.from_dict(d)
            handler(sample)

        topic = TRACK_SAMPLE_TOPIC + "/#"
        self._client.subscribe(topic)
        self._client.message_callback_add(topic, callback)

    def publish(self, sample: e.TrackSample) -> None:
        raw = self._codec.marshal(asdict(sample))
        topic = TRACK_SAMPLE_TOPIC + f"/{self._id}"
        self._client.publish(topic, raw)
