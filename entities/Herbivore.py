from Coordinates import Coordinates
from entities.Creature import Creature


class Herbivore(Creature):
    def __init__(self,  coordinates: Coordinates):
        super().__init__(coordinates, speed=1, hp=3)  # Примерные значения скорости и HP

    def __repr__(self):
        return f"Herbivore"

