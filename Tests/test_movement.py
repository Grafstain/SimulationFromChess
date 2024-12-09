import unittest

from src.simulation_from_chess import *
from src.simulation_from_chess.core import board, coordinates
from src.simulation_from_chess.entities import herbivore, grass, stone, predator
from src.simulation_from_chess.renderers import board_console_renderer


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
        
        # Сначала проверяем доступные ходы
        herbivore.update_available_moves(self.board)
        
        # Проверяем, что клетка с камнем недоступна
        self.assertNotIn(stone.coordinates, herbivore.available_moves)
        
        herbivore.make_move(self.board)
        
        # Травоядное должно выбрать обходной путь
        possible_moves = [
            Coordinates(2, 1),  # Обход слева
            Coordinates(1, 2),  # Обход сверху
            Coordinates(1, 3),  # Обход сверху дальше
            Coordinates(3, 1)   # Обход слева дальше
        ]
        self.assertTrue(
            herbivore.coordinates in possible_moves,
            f"Существо должно выбрать обходной путь. Текущие координаты: {herbivore.coordinates}"
        )

    def test_predator_speed_movement(self):
        """Тест перемещения хищника с учетом его скорости."""
        predator = Predator(Coordinates(1, 1))
        herbivore = Herbivore(Coordinates(4, 4))
        
        self.board.set_piece(predator.coordinates, predator)
        self.board.set_piece(herbivore.coordinates, herbivore)
        
        # Сначала проверяем доступные ходы
        predator.update_available_moves(self.board)
        
        # Проверяем, что все ходы в пределах скорости хищника
        for move in predator.available_moves:
            distance = abs(move.x - predator.coordinates.x) + abs(move.y - predator.coordinates.y)
            self.assertTrue(
                distance <= predator.speed,
                f"Ход {move} превышает скорость хищника {predator.speed}"
            )
        
        predator.make_move(self.board)
        
        # Хищник может переместиться на расстояние своей скорости в любом направлении
        possible_positions = [
            Coordinates(2, 2),
            Coordinates(3, 1),
            Coordinates(1, 3),
            Coordinates(2, 3),
            Coordinates(3, 2)
        ]
        self.assertTrue(
            predator.coordinates in possible_positions,
            f"Хищник должен переместиться в пределах своей скорости. Текущие координаты: {predator.coordinates}"
        )

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
        possible_moves = [
            Coordinates(1, 2),  # Движение влево
            Coordinates(2, 1)   # Движение вниз
        ]
        self.assertTrue(
            herbivore.coordinates in possible_moves,
            f"Существо должно двигаться к ближайшей траве. Текущие координаты: {herbivore.coordinates}"
        )

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
        
        # Хищник должен найти обходной путь с учетом своей скорости
        possible_moves = [
            Coordinates(1, 3),  # Обход сверху
            Coordinates(3, 1)   # Обход слева
        ]
        self.assertTrue(
            predator.coordinates in possible_moves,
            f"Хищник должен найти обходной путь. Текущие координаты: {predator.coordinates}"
        )

    def test_boundary_movement(self):
        """Тест перемещения у границ поля."""
        predator = Predator(Coordinates(0, 0))  # Угол поля
        herbivore = Herbivore(Coordinates(2, 2))
        
        self.board.set_piece(predator.coordinates, predator)
        self.board.set_piece(herbivore.coordinates, herbivore)
        
        # Проверяем доступные ходы у границы
        predator.update_available_moves(self.board)
        
        # Проверяем, что нет ходов за пределы поля
        for move in predator.available_moves:
            self.assertTrue(0 <= move.x < self.board.width)
            self.assertTrue(0 <= move.y < self.board.height)
        
        # Проверяем перемещение
        predator.make_move(self.board)
        self.assertTrue(
            0 <= predator.coordinates.x < self.board.width and
            0 <= predator.coordinates.y < self.board.height
        )

    def test_clear_path_check(self):
        """Тест проверки чистого пути до цели."""
        predator = Predator(Coordinates(1, 1))
        herbivore = Herbivore(Coordinates(4, 4))
        stone = Stone(Coordinates(2, 2))
        
        self.board.set_piece(predator.coordinates, predator)
        self.board.set_piece(herbivore.coordinates, herbivore)
        self.board.set_piece(stone.coordinates, stone)
        
        # Проверяем, что путь через камень недоступен
        self.assertFalse(
            predator.has_clear_path(self.board, Coordinates(3, 3)),
            "Путь через камень должен быть недоступен"
        )
        
        # Проверяем, что обходные пути дос��упны
        self.assertTrue(
            predator.has_clear_path(self.board, Coordinates(1, 2)),
            "Обходной путь сверху должен быть доступен"
        )
        self.assertTrue(
            predator.has_clear_path(self.board, Coordinates(2, 1)),
            "Обходной путь слева должен быть доступен"
        )

    def test_occupied_square_movement(self):
        """Тест попытки перемещения на занятую клетку."""
        herbivore1 = Herbivore(Coordinates(1, 1))
        herbivore2 = Herbivore(Coordinates(2, 2))
        grass = Grass(Coordinates(3, 3))
        
        self.board.set_piece(herbivore1.coordinates, herbivore1)
        self.board.set_piece(herbivore2.coordinates, herbivore2)
        self.board.set_piece(grass.coordinates, grass)
        
        # Проверяем доступные ходы
        herbivore1.update_available_moves(self.board)
        
        # Проверяем, что занятая клетка не входит в доступные ходы
        self.assertNotIn(herbivore2.coordinates, herbivore1.available_moves)
        
        # Проверяем, что существо выбирает свободный путь
        old_coords = herbivore1.coordinates
        herbivore1.make_move(self.board)
        self.assertNotEqual(herbivore1.coordinates, herbivore2.coordinates)

    def test_path_finding_with_obstacles(self):
        """Тест поиска пути с учетом препятствий."""
        predator = Predator(Coordinates(1, 1))
        herbivore = Herbivore(Coordinates(4, 4))
        stones = [
            Stone(Coordinates(2, 2)),
            Stone(Coordinates(3, 3))
        ]
        
        self.board.set_piece(predator.coordinates, predator)
        self.board.set_piece(herbivore.coordinates, herbivore)
        for stone in stones:
            self.board.set_piece(stone.coordinates, stone)
        
        # Проверяем доступные ходы
        predator.update_available_moves(self.board)
        
        # Проверяем, что заблокированные камнями клетки не входят в доступные ходы
        self.assertNotIn(Coordinates(2, 2), predator.available_moves)
        self.assertNotIn(Coordinates(3, 3), predator.available_moves)
        
        predator.make_move(self.board)
        
        # Все возможные обходные пути с учетом скорости хищника
        possible_moves = [
            Coordinates(1, 3),  # Обход сверху
            Coordinates(3, 1),  # Обход слева
            Coordinates(2, 3),  # Обход сверху через две клетки
            Coordinates(3, 2)   # Обход слева через две клетки
        ]
        self.assertTrue(
            predator.coordinates in possible_moves,
            f"Хищник должен найти обходной путь. Текущие координаты: {predator.coordinates}"
        )

    def test_speed_limits(self):
        """Тест ограничений скорости существ."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(4, 4))
        
        self.board.set_piece(herbivore.coordinates, herbivore)
        self.board.set_piece(grass.coordinates, grass)
        
        herbivore.make_move(self.board)
        
        # Проверяем, что существо не может переместиться дальше своей скорости
        max_distance = abs(herbivore.coordinates.x - 1) + abs(herbivore.coordinates.y - 1)
        self.assertTrue(
            max_distance <= herbivore.speed,
            f"Существо переместилось на {max_distance} клеток, что превышает его скорость {herbivore.speed}"
        )

    def test_optimal_path_selection(self):
        """Тест выбора оптимального пути к цели."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(3, 3))
        stones = [
            Stone(Coordinates(2, 2)),  # Блокируем прямой путь
            Stone(Coordinates(1, 2))   # Блокируем путь сверху
        ]
        
        self.board.set_piece(herbivore.coordinates, herbivore)
        self.board.set_piece(grass.coordinates, grass)
        for stone in stones:
            self.board.set_piece(stone.coordinates, stone)
        
        herbivore.make_move(self.board)
        
        # Единственный оптимальный путь - обход слева
        self.assertEqual(
            herbivore.coordinates,
            Coordinates(2, 1),
            f"Существо должно выбрать оптимальный путь обхода. Текущие координаты: {herbivore.coordinates}"
        )


if __name__ == '__main__':
    unittest.main()
