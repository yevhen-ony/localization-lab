from common.position import Position


class Navigation:

    def __init__(self,
        position: Position,
        step: Position,
        noise: float = 0.0, 
    ) -> None:
        self.position = position
        self.step = step
        self.noise = noise

    def forward(self) -> Position:
        self.step += Position.random(self.noise)
        self.position += self.step
        return self.position

    def backward(self) -> Position:
        self.position -= self.step
        return self.position
