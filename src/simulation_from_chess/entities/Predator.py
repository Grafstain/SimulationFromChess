from ..core import Coordinates
from ..entities.Herbivore import Herbivore
from ..entities.Creature import Creature


class Predator(Creature):
    def __init__(self, coordinates: Coordinates):
        super().__init__(coordinates, speed=2, hp=4)  # Примерные значения скорости и HP
        self.target_type = Herbivore  # Определяем тип цели

    def __repr__(self):
        return f"Predator"

