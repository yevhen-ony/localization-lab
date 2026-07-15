import time
from transport.mqtt.client import init_client
from transport.mqtt.codec import JsonCodec
import transport.mqtt.channels as chan

from .clock import Clock 


def main() -> None:
    cid, mqtt_client = init_client()

    try:
        tick_channel = chan.TickChannel(cid, mqtt_client, JsonCodec())

        clock = Clock(tick_channel) 

        mqtt_client.loop_start()

        while True:
            time.sleep(1)
            clock.emit_tick()


    except KeyboardInterrupt:
        print("Stopping the world service")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()


if __name__ == "__main__":
    main()
