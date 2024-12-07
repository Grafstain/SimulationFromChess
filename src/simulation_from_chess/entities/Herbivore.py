from ..core.Coordinates import Coordinates
from ..entities.Grass import Grass
from ..entities.Creature import Creature


class Herbivore(Creature):
    def __init__(self,  coordinates: Coordinates):
        super().__init__(coordinates, speed=1, hp=3)  # Примерные значения скорости и HP
        self.target_type = Grass  # Определяем тип цели

    def __repr__(self):
        return f"Herbivore"
