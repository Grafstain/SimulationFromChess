import Coordinates
from entities.Entity import Entity


class Stone(Entity):
    def __init__(self, coordinates: Coordinates):
        super().__init__(coordinates)