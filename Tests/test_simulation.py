import sys
import unittest
from io import StringIO
from unittest.mock import patch

from src.simulation_from_chess.core import Board, Simulation
from src.simulation_from_chess.core.Coordinates import Coordinates
from src.simulation_from_chess.entities import Herbivore, Predator, Grass
from src.simulation_from_chess.actions import SpawnGrassAction
from src.simulation_from_chess.actions.MoveAction import MoveAction
from src.simulation_from_chess.actions.HealthCheckAction import HealthCheckAction


class TestSimulation(unittest.TestCase):
    def setUp(self):
        """Создаем экземпляры необходимых классов перед каждым тестом."""
        self.simulation = Simulation()
        self.simulation.board = Board(3, 3)  # Уменьшенное поле для тестов

    def _capture_output(self):
        """Вспомогательный метод для перехвата вывода в консоль."""
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def _release_output(self):
        """Восстановление стандартного вывода."""
        sys.stdout = sys.__stdout__

    def test_simulation_initialization(self):
        """Тест инициализации симуляции."""
        self.assertEqual(self.simulation.move_counter, 0)
        self.assertFalse(self.simulation.is_running)
        self.assertFalse(self.simulation.is_paused)
        self.assertEqual(len(self.simulation.init_actions), 0)
        self.assertEqual(len(self.simulation.turn_actions), 0)

    def test_next_turn_execution(self):
        """Тест выполнения одного хода."""
        # Добавляем действие спавна травы
        self.simulation.turn_actions.append(SpawnGrassAction(min_grass=1, spawn_chance=1.0))
        
        self._capture_output()
        self.simulation.next_turn()
        output = self.held_output.getvalue()
        self._release_output()

        self.assertEqual(self.simulation.move_counter, 1)
        self.assertIn("Ход 1", output)

    def test_pause_simulation(self):
        """Тест паузы симуляции."""
        self.simulation.toggle_pause()
        self.assertTrue(self.simulation.is_paused)
        
        self.simulation.toggle_pause()
        self.assertFalse(self.simulation.is_paused)

    def test_stop_simulation(self):
        """Тест остановки симуляции."""
        self.simulation.is_running = True
        self.simulation.stop_simulation()
        self.assertFalse(self.simulation.is_running)

    def test_entity_movement(self):
        """Тест перемещения существ за один ход."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(2, 2))
        
        self.simulation.board.set_piece(herbivore.coordinates, herbivore)
        self.simulation.board.set_piece(grass.coordinates, grass)
        
        self.simulation.turn_actions.append(MoveAction())
        self.simulation.next_turn()
        
        # Проверяем, что травоядное сдвинулось с начальной позиции
        self.assertFalse(self.simulation.board.get_piece(Coordinates(1, 1)) is herbivore)

    def test_health_check_action(self):
        """Тест проверки здоровья существ."""
        herbivore = Herbivore(Coordinates(1, 1))
        herbivore.hp = 0  # Устанавливаем нулевое здоровье
        
        self.simulation.board.set_piece(herbivore.coordinates, herbivore)
        self.simulation.turn_actions.append(HealthCheckAction())
        
        self.simulation.next_turn()
        
        # Проверяем, что мертвое существо удалено с поля
        self.assertTrue(self.simulation.board.is_square_empty(Coordinates(1, 1)))

    @patch('keyboard.is_pressed')
    def test_keyboard_control(self, mock_is_pressed):
        """Тест управления симуляцией с клавиатуры."""
        # Имитируем нажатие пробела
        mock_is_pressed.side_effect = lambda key: key == 'space'
        
        self.simulation.is_running = True
        self.assertFalse(self.simulation.is_paused)
        
        # Имитируем один цикл while в start()
        if mock_is_pressed('space'):
            self.simulation.toggle_pause()
        
        self.assertTrue(self.simulation.is_paused)


if __name__ == '__main__':
    unittest.main()
