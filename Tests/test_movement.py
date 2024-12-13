import unittest
from typing import List
from src.simulation_from_chess.core.board import Board
from src.simulation_from_chess.core.coordinates import Coordinates
from src.simulation_from_chess.entities.herbivore import Herbivore
from src.simulation_from_chess.entities.predator import Predator
from src.simulation_from_chess.entities.grass import Grass
from src.simulation_from_chess.entities.stone import Stone
from src.simulation_from_chess.renderers import BoardConsoleRenderer
from src.simulation_from_chess.utils.logger import Logger
from src.simulation_from_chess.config import CREATURE_CONFIG


class TestMovement(unittest.TestCase):
    def setUp(self) -> None:
        """Создание тестового окружения."""
        self.board = Board(5, 5)
        self.logger = Logger()
        self.renderer = BoardConsoleRenderer()

    def _setup_entities(self, entities: List[tuple]) -> None:
        """Размещение сущностей на доске."""
        for entity, coords in entities:
            self.board.place_entity(coords, entity)

    def test_herbivore_grass_interaction(self) -> None:
        """Тест взаимодействия травоядного с травой."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(1, 2))
        
        # Наносим урон травоядному, чтобы оно хотело есть
        damage = 5
        herbivore.take_damage(damage)
        initial_hp = herbivore.hp
        
        self._setup_entities([
            (herbivore, herbivore.coordinates),
            (grass, grass.coordinates)
        ])
        
        # Проверяем начальное состояние
        self.assertIsNotNone(self.board.get_entity(grass.coordinates))
        
        # Используем прямое взаимодействие вместо make_move
        success, _ = herbivore.interact_with_target(self.board, grass)
        
        # Проверяем успешность взаимодействия
        self.assertTrue(success, "Взаимодействие с травой должно быть успешным")
        
        # Проверяем, что трава съедена
        self.assertIsNone(
            self.board.get_entity(grass.coordinates),
            "Трава должна быть съедена после взаимодействия"
        )
        
        # Проверяем восстановление здоровья
        expected_hp = min(
            CREATURE_CONFIG['herbivore']['initial_hp'],
            initial_hp + CREATURE_CONFIG['herbivore']['food_value']
        )
        self.assertEqual(
            herbivore.hp,
            expected_hp,
            f"HP травоядного должно восстановиться до {expected_hp}"
        )

    def test_predator_herbivore_interaction(self) -> None:
        """Тест взаимодействия хищника с травоядным."""
        predator = Predator(Coordinates(1, 1))
        herbivore = Herbivore(Coordinates(1, 2))
        
        # Устанавливаем гарантированный успех атаки
        predator.set_hunt_result(True)
        
        self._setup_entities([
            (predator, predator.coordinates),
            (herbivore, herbivore.coordinates)
        ])
        
        initial_predator_hp = predator.hp
        initial_herbivore_hp = herbivore.hp
        
        # Используем прямое взаимодействие вместо make_move
        success, _ = predator.interact_with_target(self.board, herbivore)
        
        # Проверяем успешность атаки
        self.assertTrue(success, "Атака должна ��ыть успешной")
        
        # Проверяем, что травоядное получило урон
        self.assertLess(
            herbivore.hp,
            initial_herbivore_hp,
            "Травоядное должно получить урон при успешной атаке"
        )
        
        # Проверяем восстановление здоровья хищника при успешной атаке
        if herbivore.hp <= 0:
            self.assertGreater(
                predator.hp,
                initial_predator_hp,
                "HP хищника должно увеличиться после успешной охоты"
            )

    def test_movement_collision_avoidance(self) -> None:
        """Тест избегания коллизий при движении."""
        herbivore1 = Herbivore(Coordinates(1, 1))
        herbivore2 = Herbivore(Coordinates(1, 2))
        grass = Grass(Coordinates(2, 2))
        
        self._setup_entities([
            (herbivore1, herbivore1.coordinates),
            (herbivore2, herbivore2.coordinates),
            (grass, grass.coordinates)
        ])
        
        herbivore1.make_move(self.board)
        # Проверяем, что существа не находятся на одной клет��е
        self.assertNotEqual(herbivore1.coordinates, herbivore2.coordinates)

    def test_path_finding_with_blocked_paths(self) -> None:
        """Тест поведения существа при заблокированных путях."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(2, 2))  # Трава на расстоянии 2 (манхэттенское)
        stones = [
            Stone(Coordinates(1, 2)),  # Блокируем путь вверх
            Stone(Coordinates(2, 1))   # Блокируем путь вправо
        ]
        
        # Наносим критический урон травоядному, чтобы оно хотело есть
        damage = CREATURE_CONFIG['herbivore']['initial_hp'] * 0.8
        herbivore.take_damage(int(damage))
        
        # Размещаем сущности на доске
        self._setup_entities([
            (herbivore, herbivore.coordinates),
            (grass, grass.coordinates)
        ] + [(stone, stone.coordinates) for stone in stones])
        
        # Запоминаем начальные координаты
        initial_coords = herbivore.coordinates
        
        # Получаем доступные ходы
        herbivore.update_available_moves(self.board)
        available_moves = herbivore.available_moves
        
        # Проверяем отсутствие доступных ходов
        self.assertEqual(
            len(available_moves), 
            0, 
            "При заблокированных путях не должно быть доступных ходов"
        )
        
        # Выполняем ход
        herbivore.make_move(self.board)
        
        # Проверяем, что существо не сдвинулось
        self.assertEqual(
            herbivore.coordinates,
            initial_coords,
            "Существо не должно двигаться, если все пути заблокированы"
        )

    def test_target_visibility(self) -> None:
        """Тест видимости цели."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(2, 2))
        
        self._setup_entities([
            (herbivore, herbivore.coordinates),
            (grass, grass.coordinates)
        ])
        
        manhattan_distance = self.board.manhattan_distance(
            herbivore.coordinates,
            grass.coordinates
        )
        
        self.assertLessEqual(
            manhattan_distance,
            herbivore.speed * 2,
            "Трава должна быть в пределах видимости существа"
        )

    def test_orthogonal_movement(self) -> None:
        """Тест ортогональности движения."""
        herbivore = Herbivore(Coordinates(2, 2))
        
        self._setup_entities([
            (herbivore, herbivore.coordinates)
        ])
        
        herbivore.update_available_moves(self.board)
        available_moves = herbivore.available_moves
        
        # Проверяем, что все доступные ходы - ортогональные
        initial_coords = herbivore.coordinates
        for move in available_moves:
            dx = abs(move.x - initial_coords.x)
            dy = abs(move.y - initial_coords.y)
            self.assertTrue(
                (dx == 1 and dy == 0) or (dx == 0 and dy == 1),
                "Доступные ходы должны быть только ортогональными"
            )

    def test_movement_speed_limit(self) -> None:
        """Тест ограничения скорости движения."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(4, 4))
        
        self._setup_entities([
            (herbivore, herbivore.coordinates),
            (grass, grass.coordinates)
        ])
        
        initial_coords = herbivore.coordinates
        herbivore.make_move(self.board)
        
        # Провряем, что асстояние перемещения не превышает скорость
        manhattan_distance = (
            abs(herbivore.coordinates.x - initial_coords.x) +
            abs(herbivore.coordinates.y - initial_coords.y)
        )
        self.assertLessEqual(manhattan_distance, herbivore.speed)

if __name__ == '__main__':
    unittest.main()
