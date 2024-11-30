import Coordinates
from Creature import Creature


class Predator(Creature):
    def __init__(self, coordinates: Coordinates):
        super().__init__(coordinates, speed=2, hp=4)  # Примерные значения скорости и HP
        self.attack_power = 2  # Сила атаки
