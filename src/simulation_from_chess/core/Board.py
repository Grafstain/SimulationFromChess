from . import Coordinates
from ..core import *


class Board:
    def __init__(self, width: int = 8, height: int = 8):
        self.width = width
        self.height = height
        self.entities: Dict[Coordinates, Entity] = {}
        # self.moves: List[Move] = []

    def set_piece(self, coordinates: Coordinates, entity: Entity):
        if not self.is_square_empty(coordinates):
            return
        entity.coordinates = coordinates
        self.entities[coordinates] = entity

    def remove_piece(self, coordinates: Coordinates):
        if coordinates in self.entities:
            del self.entities[coordinates]

    def is_square_empty(self, coordinates: Coordinates) -> bool:
        return coordinates not in self.entities

    def get_piece(self, coordinates: Coordinates) -> Entity:
        return self.entities.get(coordinates)

    def setup_fixed_positions(self):
        """Устанавливает фиксированные позиции для травоядных и хищников."""
        fixed_herbivores_positions = [
            Coordinates(1, 1),
            Coordinates(2, 3),
            Coordinates(3, 5),
            Coordinates(4, 7),
            Coordinates(5, 2)
        ]

        fixed_predators_positions = [
            Coordinates(6, 1),
            Coordinates(7, 3),
            Coordinates(8, 5)
        ]

        # Установка травоядных
        for coord in fixed_herbivores_positions:
            if self.is_square_empty(coord):
                herbivore = Herbivore(coord)
                self.set_piece(coord, herbivore)
            else:
                print(f"Cannot place herbivore at {coord}, square is already occupied.")

        # Установка хищников
        for coord in fixed_predators_positions:
            if self.is_square_empty(coord):
                predator = Predator(coord)
                self.set_piece(coord, predator)
            else:
                print(f"Cannot place predator at {coord}, square is already occupied.")

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
