from Coordinates import Coordinates
from Entity import Entity


class Creature(Entity):
    def __init__(self, coordinates: Coordinates, speed: int, hp: int):
        super().__init__(coordinates)
        self.speed = speed  # Скорость передвижения
        self.hp = hp  # Очки здоровья
