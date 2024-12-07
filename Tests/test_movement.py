import unittest

from src.simulation_from_chess import *
from src.simulation_from_chess.core import Board, Coordinates
from src.simulation_from_chess.entities import Herbivore, Grass, Stone, Predator
from src.simulation_from_chess.renderers import BoardConsoleRenderer


class TestMovement(unittest.TestCase):
    def setUp(self):
        """Создаем экземпляры необходимых классов перед каждым тестом."""
        self.board = Board(5, 5)
        self.renderer = BoardConsoleRenderer()

    def test_basic_herbivore_movement(self):
        """Тест базового перемещения травоядного к траве."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(2, 2))
        
        self.board.set_piece(herbivore.coordinates, herbivore)
        self.board.set_piece(grass.coordinates, grass)
        
        herbivore.make_move(self.board)
        
        # Травоядное должно переместиться на одну клетку ближе к траве
        self.assertTrue(
            herbivore.coordinates in [Coordinates(2, 1), Coordinates(1, 2)]
        )
        self.assertTrue(self.board.is_square_empty(Coordinates(1, 1)))

    def test_herbivore_blocked_movement(self):
        """Тест перемещения травоядного при заблокированном пути."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(3, 3))
        stone = Stone(Coordinates(2, 2))  # Камень блокирует прямой путь
        
        self.board.set_piece(herbivore.coordinates, herbivore)
        self.board.set_piece(grass.coordinates, grass)
        self.board.set_piece(stone.coordinates, stone)
        
        herbivore.make_move(self.board)
        
        # Травоядное должно выбрать обходной путь
        self.assertTrue(
            herbivore.coordinates in [Coordinates(2, 1), Coordinates(1, 2)]
        )

    def test_predator_speed_movement(self):
        """Тест перемещения хищника с учетом его скорости."""
        predator = Predator(Coordinates(1, 1))
        herbivore = Herbivore(Coordinates(4, 4))
        
        self.board.set_piece(predator.coordinates, predator)
        self.board.set_piece(herbivore.coordinates, herbivore)
        
        predator.make_move(self.board)
        
        # Хищник может переместиться на 2 клетки в любом направлении
        possible_positions = [
            Coordinates(2, 2),
            Coordinates(3, 1),
            Coordinates(1, 3)
        ]
        self.assertTrue(predator.coordinates in possible_positions)

    def test_no_available_moves(self):
        """Тест поведения существа, когда нет доступных ходов."""
        herbivore = Herbivore(Coordinates(1, 1))
        # Окружаем травоядное камнями
        stones = [
            Stone(Coordinates(1, 2)),
            Stone(Coordinates(2, 1)),
            Stone(Coordinates(2, 2))
        ]
        
        self.board.set_piece(herbivore.coordinates, herbivore)
        for stone in stones:
            self.board.set_piece(stone.coordinates, stone)
            
        old_coordinates = herbivore.coordinates
        herbivore.make_move(self.board)
        
        # Существо должно остаться на месте
        self.assertEqual(herbivore.coordinates, old_coordinates)

    def test_multiple_targets(self):
        """Тест выбора ближайшей цели при наличии нескольких."""
        herbivore = Herbivore(Coordinates(2, 2))
        grass_pieces = [
            Grass(Coordinates(1, 1)),  # Ближайшая трава
            Grass(Coordinates(4, 4)),
            Grass(Coordinates(1, 4))
        ]
        
        self.board.set_piece(herbivore.coordinates, herbivore)
        for grass in grass_pieces:
            self.board.set_piece(grass.coordinates, grass)
            
        herbivore.make_move(self.board)
        
        # Травоядное должно двигаться к ближайшей траве
        self.assertEqual(herbivore.coordinates, Coordinates(1, 2))

    def test_path_finding(self):
        """Тест поиска пути в сложной ситуации."""
        predator = Predator(Coordinates(1, 1))
        herbivore = Herbivore(Coordinates(4, 4))
        stones = [
            Stone(Coordinates(2, 2)),
            Stone(Coordinates(2, 3)),
            Stone(Coordinates(3, 2))
        ]
        
        self.board.set_piece(predator.coordinates, predator)
        self.board.set_piece(herbivore.coordinates, herbivore)
        for stone in stones:
            self.board.set_piece(stone.coordinates, stone)
            
        predator.make_move(self.board)
        
        # Хищник должен найти обходной путь
        self.assertTrue(
            predator.coordinates in [Coordinates(1, 3), Coordinates(3, 1)]
        )

    def test_boundary_movement(self):
        """Тест поведения существа у границы доски."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(1, 2))
        
        self.board.set_piece(herbivore.coordinates, herbivore)
        self.board.set_piece(grass.coordinates, grass)
        
        herbivore.make_move(self.board)
        
        # Проверяем, что существо не вышло за пределы доски
        self.assertTrue(1 <= herbivore.coordinates.x <= self.board.width)
        self.assertTrue(1 <= herbivore.coordinates.y <= self.board.height)


if __name__ == '__main__':
    unittest.main()
