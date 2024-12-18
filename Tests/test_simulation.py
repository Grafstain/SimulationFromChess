from unittest import TestCase
from unittest.mock import patch, MagicMock
from io import StringIO
from src.simulation_from_chess import (
    Simulation,
    Coordinates,
    Herbivore,
    Predator,
    Grass,
    Creature,
    Action
)

class TestSimulation(TestCase):
    def setUp(self):
        """Подготовка окружения для каждого теста."""
        self.simulation = Simulation(size=10)
        self.board = self.simulation.board
        # Очищаем доску для чистоты тестов
        self.board.entities.clear()
        self.simulation.is_running = False
        
    def _add_test_creature(self):
        """Вспомогательный метод для добавления тестового существа."""
        herbivore = Herbivore(Coordinates(1, 1))
        self.simulation.place_entity(herbivore, herbivore.coordinates)
        return herbivore
        
    def test_initial_state(self):
        """Тест начального состояния симуляции."""
        self.assertEqual(self.board.width, 10)
        self.assertEqual(self.board.height, 10)
        self.assertEqual(self.simulation.move_counter, 0)
        self.assertFalse(self.simulation.is_running)
        self.assertFalse(self.simulation.is_paused)
        self.assertEqual(len(self.simulation.turn_actions), 0)

    def test_initialization_with_entities(self):
        """Тест инициализации симуляции с сущностями."""
        # Проверяем, что доска пуста перед инициализацией
        self.assertEqual(len(self.board.entities), 0)
        
        # Проверяем, что на доске достаточно места
        total_entities = 6  # 2 травоядных + 1 хищник + 3 травы
        board_size = self.board.width * self.board.height
        self.assertGreaterEqual(
            board_size, total_entities,
            f"Размер доски ({board_size}) должен быть больше количества сущностей ({total_entities})"
        )
        
        # Проверяем инициализацию с существами
        self.simulation.initialize(herbivores=2, predators=1, grass=3)
        
        # Проверяем, что все сущности были размещены
        entity_counts = {
            Herbivore: 0,
            Predator: 0,
            Grass: 0
        }
        
        for entity in self.board.entities.values():
            if type(entity) in entity_counts:
                entity_counts[type(entity)] += 1
        
        # Проверяем точное количество каждого типа сущностей
        self.assertEqual(
            entity_counts[Herbivore], 2,
            f"Неверное количество травоядных: {entity_counts[Herbivore]} вместо 2"
        )
        self.assertEqual(
            entity_counts[Predator], 1,
            f"Неверное количество хищников: {entity_counts[Predator]} вместо 1"
        )
        self.assertEqual(
            entity_counts[Grass], 3,
            f"Неверное количество травы: {entity_counts[Grass]} вместо 3"
        )
        
        # После инициализации с существами симуляция должна быть запущена
        self.assertTrue(self.simulation.is_running)

    def test_simulation_steps(self):
        """Тест выполнения шагов симуляции."""
        herbivore = self._add_test_creature()
        
        with patch('keyboard.is_pressed', return_value=False), patch('time.sleep'):
            self.simulation.run(steps=3)
        
        self.assertEqual(self.simulation.move_counter, 3)
        self.assertTrue(self.simulation.is_running)
        self.assertTrue(herbivore.hp > 0)

    def test_action_execution(self):
        """Тест выполнения действий в правильном порядке."""
        executed_actions = []
        
        class TestAction(Action):
            def __init__(self, name):
                self.name = name
            def execute(self, board, logger):
                executed_actions.append(self.name)
        
        # Настраиваем тестовые действия
        actions = ['SpawnGrass', 'Move', 'Hunger']
        self.simulation.turn_actions = [TestAction(name) for name in actions]
        
        # Добавляем существо и выполняем ход
        self._add_test_creature()
        with patch('sys.stdout', new=StringIO()):
            self.simulation.next_turn()
        
        self.assertEqual(executed_actions, actions)

    def test_lifecycle_states(self):
        """Тест жизненного цикла симуляции."""
        # Проверяем начальное состояние
        self.assertFalse(self.simulation.is_running)
        
        # Добавляем существо
        herbivore = self._add_test_creature()
        self.assertTrue(self.simulation.is_running)
        
        # Проверяем работу с живым существом
        with patch('sys.stdout', new=StringIO()):
            self.assertTrue(self.simulation.next_turn())
        
        # Проверяем завершение при смерти существа
        herbivore.hp = 0
        with patch('sys.stdout', new=StringIO()):
            self.assertFalse(self.simulation.next_turn())
            self.assertFalse(self.simulation.is_running)

    def test_empty_board(self):
        """Тест работы с пустой доской."""
        # Проверяем, что доска действительно пуста
        self.assertEqual(len(self.board.entities), 0)
        
        with patch('sys.stdout', new=StringIO()):
            self.assertFalse(self.simulation.next_turn())
        self.assertFalse(self.simulation.is_running)
        self.assertEqual(self.simulation.move_counter, 0)

    def test_simulation_control(self):
        """Тест управления симуляцией (остановка/пауза)."""
        self._add_test_creature()
        
        # Тест остановки
        self.simulation.stop_simulation()
        with patch('sys.stdout', new=StringIO()):
            self.assertFalse(self.simulation.next_turn())
        
        # Тест паузы
        self.simulation.is_running = True
        self.simulation.toggle_pause()
        self.assertTrue(self.simulation.is_paused)

    def test_entity_placement_coordinates(self):
        """Тест валидности координат при размещении существ."""
        self.simulation.initialize(herbivores=5, predators=3, grass=4)
        
        # Проверяем, что все сущности размещены в пределах доски
        for entity in self.board.entities.values():
            coords = entity.coordinates
            self.assertTrue(
                1 <= coords.x <= self.board.width,
                f"X-координата {coords.x} вне пределов доски (1-{self.board.width})"
            )
            self.assertTrue(
                1 <= coords.y <= self.board.height,
                f"Y-координата {coords.y} вне пределов доски (1-{self.board.height})"
            )
