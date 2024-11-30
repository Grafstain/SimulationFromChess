from abc import ABC
from Coordinates import Coordinates


class Creature(ABC):
    def __init__(self, coordinates: Coordinates, speed: int, hp: int):
        self.coordinates = coordinates  # Координаты на доске
        self.speed = speed  # Скорость передвижения
        self.hp = hp  # Очки здоровья
