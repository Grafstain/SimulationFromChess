import random
from typing import Dict

from Coordinates import Coordinates
from Entity import Entity
from Herbivore import Herbivore
from Predator import Predator


class Board:
    def __init__(self, width: int = 8, height: int = 8):
        self.width = width
        self.height = height
        self.entities: Dict[Coordinates, Entity] = {}
        # self.moves: List[Move] = []

    def set_piece(self, coordinates: Coordinates, entity: Entity):
        entity.coordinates = coordinates
        self.entities[coordinates] = entity

    def remove_piece(self, coordinates: Coordinates):
        if coordinates in self.entities:
            del self.entities[coordinates]

    def is_square_empty(self, coordinates: Coordinates) -> bool:
        return coordinates not in self.entities

    def get_piece(self, coordinates: Coordinates) -> Entity:
        return self.entities.get(coordinates)

    def setup_random_positions(self):
        herbivores_count = 5
        predators_count = 3
        all_coordinates = [Coordinates(x, y) for x in range(self.width) for y in range(self.height)]
        random.shuffle(all_coordinates)  # Перемешиваем координаты для случайного выбора
        for i in range(herbivores_count):
            if i < len(all_coordinates):
                coord = all_coordinates[i]
                herbivore = Herbivore(coord)
                self.set_piece(coord, herbivore)
                # print(f"Placed Herbivore at {coord.__repr__()}")

        for i in range(predators_count):
            if i + herbivores_count < len(all_coordinates):
                coord = all_coordinates[i + herbivores_count]
                predator = Predator(coord)
                self.set_piece(coord, predator)
                # print(f"Placed Predator at {coord.__repr__()}")

    @staticmethod
    def is_square_dark(coordinates: Coordinates) -> bool:
        return (coordinates.x + coordinates.y) % 2 == 0
