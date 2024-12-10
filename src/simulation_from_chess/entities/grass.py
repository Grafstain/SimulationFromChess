from ..core.coordinates import Coordinates
from ..entities.entity import Entity


class Grass(Entity):
    def __init__(self, coordinates: Coordinates):
        super().__init__(coordinates)

    def __repr__(self):
        """Строковое представление травы."""
        return "Трава"