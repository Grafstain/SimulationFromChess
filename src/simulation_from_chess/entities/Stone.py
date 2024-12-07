from ..core import Coordinates
from ..entities import Entity


class Stone(Entity):
    def __init__(self, coordinates: Coordinates):
        super().__init__(coordinates)