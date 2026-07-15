from common.entities import Tick
from transport.protocols import TickChannel


class Clock:
    def __init__(self, tick_channel: TickChannel):
        self._tick_channel = tick_channel
        self._epoch = 0
        self._slots = 30

    def emit_tick(self) -> None:
        self._epoch += 1

        tick = Tick(
            epoch=self._epoch,
            slots=self._slots,
        )

        self._tick_channel.publish(tick)
