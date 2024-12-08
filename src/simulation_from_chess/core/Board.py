import random
from typing import Dict

from src.simulation_from_chess.core.Coordinates import Coordinates
from src.simulation_from_chess.entities import Entity, Herbivore, Predator, Grass, Stone
from src.simulation_from_chess.utils.Logger import Logger


class Board:
    def __init__(self, width: int = 8, height: int = 8):
        self.width = width
        self.height = height
        self.entities: Dict[Coordinates, Entity] = {}

    def set_piece(self, coordinates: Coordinates, entity: Entity):
        """Установка существа на поле с проверкой границ."""
        if not self.is_valid_coordinates(coordinates) or not self.is_square_empty(coordinates):
            return False
        entity.coordinates = coordinates
        self.entities[coordinates] = entity
        return True

    def remove_piece(self, coordinates: Coordinates):
        if coordinates in self.entities:
            del self.entities[coordinates]

    def is_square_empty(self, coordinates: Coordinates) -> bool:
        """Проверка пустой ли квадрат."""
        if not self.is_valid_coordinates(coordinates):
            return False
        return coordinates not in self.entities

    def get_piece(self, coordinates: Coordinates) -> Entity:
        """Получение существа с проверкой валидности координат."""
        if not self.is_valid_coordinates(coordinates):
            return None
        return self.entities.get(coordinates)

    def setup_fixed_positions(self):
        """Устанавливает начальные позиции существ."""
        all_coordinates = [
            Coordinates(x, y)
            for x in range(1, self.width + 1)
            for y in range(1, self.height + 1)
        ]
        random.shuffle(all_coordinates)
        # ... остальной код метода без изменений ...

    def setup_random_positions(self):
        herbivores_count = 5
        predators_count = 3
        grass_count = 4
        stone_count = 2

        all_coordinates = [Coordinates(x, y) for x in range(self.width) for y in range(self.height)]
        random.shuffle(all_coordinates)  # Перемешиваем координаты для случайного выбора

        # Установка травоядных
        placed_herbivores = 0
        for coord in all_coordinates:
            if placed_herbivores <= herbivores_count and self.is_square_empty(coord):
                herbivore = Herbivore(coord)
                self.set_piece(coord, herbivore)
                placed_herbivores += 1
                all_coordinates.remove(coord)

        # Установка хищников
        placed_predator = 0
        for coord in all_coordinates:
            if placed_predator <= predators_count and self.is_square_empty(coord):
                predator = Predator(coord)
                self.set_piece(coord, predator)
                placed_predator += 1
                all_coordinates.remove(coord)

        # Установка травы
        placed_grass = 0
        for coord in all_coordinates:
            if placed_grass <= grass_count and self.is_square_empty(coord):
                grass = Grass(coord)
                self.set_piece(coord, grass)
                placed_grass += 1
                all_coordinates.remove(coord)

        # Установка камней
        placed_stone = 0
        for coord in all_coordinates:
            if placed_stone <= stone_count and self.is_square_empty(coord):
                stone = Stone(coord)
                self.set_piece(coord, stone)
                placed_stone += 1
                all_coordinates.remove(coord)

    @staticmethod
    def is_square_dark(coordinates: Coordinates) -> bool:
        return (coordinates.x + coordinates.y) % 2 == 0

    def is_valid_coordinates(self, coordinates: Coordinates) -> bool:
        """Проверка валидности координат."""
        return (1 <= coordinates.x <= self.width and 
                1 <= coordinates.y <= self.height)
