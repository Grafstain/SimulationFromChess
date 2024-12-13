from ..core.coordinates import Coordinates
from ..entities.entity import Entity


class Stone(Entity):
    def __init__(self, coordinates: Coordinates):
        super().__init__(coordinates)

    def __repr__(self):
        """Строковое представление камня."""
        return "Камень"