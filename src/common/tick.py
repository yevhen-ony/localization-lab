from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Tick:
    epoch: int
    span: int
    slots: int
