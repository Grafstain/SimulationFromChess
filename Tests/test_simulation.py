import sys
import unittest
from io import StringIO
from unittest.mock import patch, Mock
from typing import Type

from src.simulation_from_chess.core.board import Board
from src.simulation_from_chess.core.coordinates import Coordinates
from src.simulation_from_chess.core.simulation import Simulation
from src.simulation_from_chess.entities.grass import Grass
from src.simulation_from_chess.entities.herbivore import Herbivore
from src.simulation_from_chess.entities.predator import Predator
from src.simulation_from_chess.actions.move_action import MoveAction
from src.simulation_from_chess.actions.health_check_action import HealthCheckAction
from src.simulation_from_chess.actions.spawn_grass_action import SpawnGrassAction
from src.simulation_from_chess.actions.hunger_action import HungerAction
from src.simulation_from_chess.actions.init_action import InitAction
from src.simulation_from_chess.config import SIMULATION_CONFIG, CREATURE_CONFIG


class TestSimulation(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения."""
        self.simulation = Simulation(board_size=5)
        self.board = self.simulation.board
        
        # Добавляем базовые действия
        self.simulation.turn_actions = [
            SpawnGrassAction(min_grass=1, spawn_chance=1.0),
            MoveAction(),
            HungerAction(hunger_damage=1),
            HealthCheckAction()
        ]

    def _count_entities(self, entity_type: Type) -> int:
        """Подсчет количества сущностей определенного типа."""
        return len(self.board.get_entities_by_type(entity_type))

    def test_simulation_initialization(self):
        """Тест инициализации симуляции."""
        self.assertEqual(self.board.width, 5)
        self.assertEqual(self.board.height, 5)
        self.assertEqual(len(self.simulation.turn_actions), 4)
        self.assertFalse(self.simulation.is_running)
        self.assertFalse(self.simulation.is_paused)
        self.assertEqual(self.simulation.move_counter, 0)

    def test_invalid_board_size(self):
        """Тест создания симуляции с невалидным размером поля."""
        with self.assertRaises(ValueError):
            Simulation(board_size=0)
        with self.assertRaises(ValueError):
            Simulation(board_size=-1)

    def test_simulation_lifecycle(self):
        """Тест жизненного цикла симуляции."""
        # Инициализация
        self.simulation.initialize(herbivores=2, predators=1, grass=3)
        
        # Проверка начального состояния
        self.assertEqual(self._count_entities(Herbivore), 2)
        self.assertEqual(self._count_entities(Predator), 1)
        self.assertEqual(self._count_entities(Grass), 3)
        
        # Проверка выполнения одного хода
        with patch('sys.stdout', new=StringIO()):
            self.simulation.next_turn()
        
        # Проверка изменения состояния после хода
        self.assertEqual(self.simulation.move_counter, 1)
        self.assertTrue(
            self._count_entities(Herbivore) <= 2 and
            self._count_entities(Predator) <= 1 and
            self._count_entities(Grass) >= 3
        )

    def test_simulation_controls(self):
        """Тест управления симуляцией (пауза/возобновление/остановка)."""
        self.simulation.initialize(herbivores=1, predators=1, grass=1)
        
        # Тест запуска
        self.simulation.start(run_loop=False)
        self.assertTrue(self.simulation.is_running)
        
        # Проверяем, что ход выполняется без паузы
        initial_counter = self.simulation.move_counter
        with patch('sys.stdout', new=StringIO()):
            result = self.simulation.next_turn()
        self.assertTrue(result)
        self.assertEqual(self.simulation.move_counter, initial_counter + 1)
        
        # Тест паузы
        self.simulation.toggle_pause()
        self.assertTrue(self.simulation.is_paused)
        paused_counter = self.simulation.move_counter
        
        # Проверяем, что во время паузы ход не выполняется
        with patch('sys.stdout', new=StringIO()):
            result = self.simulation.next_turn()
        self.assertFalse(result)
        self.assertEqual(self.simulation.move_counter, paused_counter)
        
        # Тест возобновления
        self.simulation.toggle_pause()
        self.assertFalse(self.simulation.is_paused)
        with patch('sys.stdout', new=StringIO()):
            result = self.simulation.next_turn()
        self.assertTrue(result)
        self.assertEqual(self.simulation.move_counter, paused_counter + 1)
        
        # Тест остановки
        self.simulation.stop_simulation()
        self.assertFalse(self.simulation.is_running)

    def test_run_with_steps(self):
        """Тест запуска симуляции на определенное количество шагов."""
        self.simulation.initialize(herbivores=1, predators=1, grass=1)
        
        with patch('keyboard.is_pressed', return_value=False):
            with patch('time.sleep'):
                self.simulation.run(steps=3)
        
        self.assertEqual(self.simulation.move_counter, 3)

    def test_empty_board_simulation_stop(self):
        """Тест автоматической остановки симуляции при отсутствии существ."""
        # Инициализируем только траву
        self.simulation.initialize(grass=1)
        
        with patch('sys.stdout', new=StringIO()):
            result = self.simulation.next_turn()
        
        self.assertFalse(result)
        self.assertFalse(self.simulation.is_running)

    def test_action_execution_order(self):
        """Тест порядка выполнения действий."""
        executed_actions = []
        
        class TestAction:
            def __init__(self, name):
                self.name = name
                
            def execute(self, board, logger):
                executed_actions.append(self.name)
        
        # Создаем тестовые действия
        self.simulation.turn_actions = [
            TestAction('Action1'),
            TestAction('Action2'),
            TestAction('Action3')
        ]
        
        # Добавляем существо, чтобы симуляция не остановилась
        herbivore = Herbivore(Coordinates(1, 1))
        self.board.place_entity(herbivore.coordinates, herbivore)
        
        with patch('sys.stdout', new=StringIO()):
            self.simulation.next_turn()
        
        # Проверяем количество и порядок выполнения действий
        self.assertEqual(len(executed_actions), 3)
        self.assertEqual(
            executed_actions,
            ['Action1', 'Action2', 'Action3']
        )


if __name__ == '__main__':
    unittest.main()
