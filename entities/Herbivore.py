from ..Coordinates import Coordinates
from .Creature import Creature
from .Grass import Grass


class Herbivore(Creature):
    def __init__(self,  coordinates: Coordinates):
        super().__init__(coordinates, speed=1, hp=3)  # Примерные значения скорости и HP
        self.target_type = Grass  # Определяем тип цели

    def __repr__(self):
        return f"Herbivore"

