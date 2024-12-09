import unittest
from typing import List

from src.simulation_from_chess.core.board import Board
from src.simulation_from_chess.core.coordinates import Coordinates
from src.simulation_from_chess.entities.grass import Grass
from src.simulation_from_chess.entities.herbivore import Herbivore
from src.simulation_from_chess.entities.predator import Predator
from src.simulation_from_chess.entities.stone import Stone
from src.simulation_from_chess.renderers.board_console_renderer import BoardConsoleRenderer


class TestMovement(unittest.TestCase):
    def setUp(self) -> None:
        """Создание тестового окружения."""
        self.board = Board(5, 5)
        self.renderer = BoardConsoleRenderer()

    def _setup_entities(self, entities: List[tuple]) -> None:
        """
        Вспомогательный метод для размещения сущностей на доске.
        
        Args:
            entities: Список кортежей (сущность, координаты)
        """
        for entity, coords in entities:
            self.board.place_entity(coords, entity)

    def _calculate_distance(self, coords1: Coordinates, coords2: Coordinates) -> int:
        """
        Вычисление манхэттенского расстояния между координатами.
        
        Args:
            coords1: Первые координаты
            coords2: Вторые координаты
        Returns:
            int: Манхэттенское расстояние
        """
        return (abs(coords1.x - coords2.x) + abs(coords1.y - coords2.y))

    def test_basic_herbivore_movement(self) -> None:
        """Тест базового перемещения травоядного к траве."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(2, 2))
        
        self._setup_entities([(herbivore, herbivore.coordinates), 
                            (grass, grass.coordinates)])
        
        herbivore.make_move(self.board)
        
        possible_moves = [Coordinates(2, 1), Coordinates(1, 2)]
        self.assertIn(herbivore.coordinates, possible_moves)
        self.assertTrue(self.board.is_position_vacant(Coordinates(1, 1)))

    def test_herbivore_blocked_movement(self) -> None:
        """Тест перемещения травоядного при заблокированном пути."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(3, 3))
        stone = Stone(Coordinates(2, 2))
        
        self._setup_entities([
            (herbivore, herbivore.coordinates),
            (grass, grass.coordinates),
            (stone, stone.coordinates)
        ])
        
        herbivore.update_available_moves(self.board)
        initial_coords = herbivore.coordinates
        
        self.assertNotIn(stone.coordinates, herbivore.available_moves)
        
        herbivore.make_move(self.board)
        
        self.assertNotEqual(herbivore.coordinates, initial_coords)
        self.assertNotEqual(herbivore.coordinates, stone.coordinates)
        
        current_distance = self._calculate_distance(herbivore.coordinates, grass.coordinates)
        initial_distance = self._calculate_distance(initial_coords, grass.coordinates)
        self.assertLess(current_distance, initial_distance)

    def test_predator_speed_movement(self) -> None:
        """Тест перемещения хищника с учетом его скорости."""
        predator = Predator(Coordinates(1, 1))
        herbivore = Herbivore(Coordinates(4, 4))
        
        self._setup_entities([
            (predator, predator.coordinates),
            (herbivore, herbivore.coordinates)
        ])
        
        initial_coords = predator.coordinates
        predator.make_move(self.board)
        
        distance_moved = self._calculate_distance(predator.coordinates, initial_coords)
        self.assertLessEqual(distance_moved, predator.speed)
        
        current_distance = self._calculate_distance(predator.coordinates, herbivore.coordinates)
        initial_distance = self._calculate_distance(initial_coords, herbivore.coordinates)
        self.assertLess(current_distance, initial_distance)

    def test_no_available_moves(self) -> None:
        """Тест поведения существа без доступных ходов."""
        herbivore = Herbivore(Coordinates(1, 1))
        stones = [
            Stone(Coordinates(1, 2)),
            Stone(Coordinates(2, 1)),
            Stone(Coordinates(2, 2))
        ]
        
        self._setup_entities([(herbivore, herbivore.coordinates)] + 
                           [(stone, stone.coordinates) for stone in stones])
        
        old_coordinates = herbivore.coordinates
        herbivore.make_move(self.board)
        self.assertEqual(herbivore.coordinates, old_coordinates)

    def test_multiple_targets(self) -> None:
        """Тест выбора ближайшей цели при наличии нескольких."""
        herbivore = Herbivore(Coordinates(2, 2))
        grass_pieces = [
            Grass(Coordinates(1, 1)),
            Grass(Coordinates(4, 4)),
            Grass(Coordinates(1, 4))
        ]
        
        self._setup_entities([(herbivore, herbivore.coordinates)] + 
                           [(grass, grass.coordinates) for grass in grass_pieces])
        
        herbivore.make_move(self.board)
        possible_moves = [Coordinates(1, 2), Coordinates(2, 1)]
        
        self.assertIn(
            herbivore.coordinates, 
            possible_moves,
            f"Существо должно двигаться к ближайшей траве. Текущие координаты: {herbivore.coordinates}"
        )

    def test_path_finding(self) -> None:
        """Тест поиска пути в сложной ситуации."""
        predator = Predator(Coordinates(1, 1))
        herbivore = Herbivore(Coordinates(4, 4))
        stones = [
            Stone(Coordinates(2, 2)),
            Stone(Coordinates(2, 3)),
            Stone(Coordinates(3, 2))
        ]
        
        self._setup_entities([(predator, predator.coordinates),
                            (herbivore, herbivore.coordinates)] + 
                           [(stone, stone.coordinates) for stone in stones])
        
        initial_coords = predator.coordinates
        predator.make_move(self.board)
        
        # Проверяем, что хищник сделал допустимый ход
        self.assertNotEqual(predator.coordinates, initial_coords)
        
        # Проверяем, что хищник не оказался на камне
        for stone in stones:
            self.assertNotEqual(predator.coordinates, stone.coordinates)
        
        # Проверяем, что хищник приблизился к цели
        current_distance = self._calculate_distance(predator.coordinates, herbivore.coordinates)
        initial_distance = self._calculate_distance(initial_coords, herbivore.coordinates)
        self.assertLess(
            current_distance, 
            initial_distance,
            f"Хищник должен приближаться к цели. Начальное расстояние: {initial_distance}, "
            f"текущее расстояние: {current_distance}"
        )
        
        # Проверяем, что перемещение соответствует скорости хищника
        move_distance = self._calculate_distance(initial_coords, predator.coordinates)
        self.assertLessEqual(
            move_distance, 
            predator.speed,
            f"Дистанция перемещения ({move_distance}) не должна превышать скорость хищника ({predator.speed})"
        )

    def test_occupied_square_movement(self) -> None:
        """Тест попытки перемещения на занятую клетку."""
        herbivore1 = Herbivore(Coordinates(1, 1))
        herbivore2 = Herbivore(Coordinates(2, 2))
        grass = Grass(Coordinates(3, 3))
        
        self._setup_entities([
            (herbivore1, herbivore1.coordinates),
            (herbivore2, herbivore2.coordinates),
            (grass, grass.coordinates)
        ])
        
        herbivore1.update_available_moves(self.board)
        self.assertNotIn(herbivore2.coordinates, herbivore1.available_moves)
        
        old_coords = herbivore1.coordinates
        herbivore1.make_move(self.board)
        self.assertNotEqual(herbivore1.coordinates, herbivore2.coordinates)

    def test_multi_turn_movement(self) -> None:
        """Тест движения к удаленной цели за несколько ходов."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(5, 5))
        
        self._setup_entities([
            (herbivore, herbivore.coordinates),
            (grass, grass.coordinates)
        ])
        
        initial_coords = herbivore.coordinates
        herbivore.make_move(self.board)
        
        first_move_distance = self._calculate_distance(herbivore.coordinates, initial_coords)
        self.assertEqual(first_move_distance, herbivore.speed)
        
        position_after_first_move = Coordinates(herbivore.coordinates.x, herbivore.coordinates.y)
        
        herbivore.update_available_moves(self.board)
        herbivore.make_move(self.board)
        
        second_move_distance = self._calculate_distance(herbivore.coordinates, position_after_first_move)
        self.assertLessEqual(second_move_distance, herbivore.speed)


if __name__ == '__main__':
    unittest.main()
