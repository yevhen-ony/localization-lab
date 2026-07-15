from common.position import Position, Velocity


class Navigation:

    def __init__(self,
        position: Position,
        velocity: Velocity,
        noise: float = 0.0, 
    ) -> None:
        self.position = position
        self.velocity = velocity 
        self.noise = noise

    def advance(self, dt: float) -> Position:
        velocity = self.velocity + Velocity.random(self.noise)
        self.position += velocity.step(dt)
        return self.position

    def turn(self, dt: float) -> Position:
        self.velocity *= -1
        return self.advance(dt)


