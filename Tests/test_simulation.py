import sys
import unittest
from io import StringIO
from unittest.mock import patch
from typing import List

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
        self.simulation = Simulation(board_size=5)  # Уменьшенное поле для тестов
        self.board = self.simulation.board

    def _capture_output(self):
        """Вспомогательный метод для перехвата вывода в консоль."""
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def _release_output(self):
        """Восстановление стандартного вывода."""
        sys.stdout = sys.__stdout__

    def test_spawn_grass_action(self):
        """Тест спавна травы."""
        spawn_action = SpawnGrassAction(min_grass=1, spawn_chance=1.0)  # Гарантированный спавн
        
        # Проверяем начальное состояние
        initial_grass = self._count_entities(Grass)
        self.assertEqual(initial_grass, 0)
        
        # Выполняем действие
        spawn_action.execute(self.board, self.simulation.logger)
        
        # Проверяем результат
        final_grass = self._count_entities(Grass)
        self.assertEqual(final_grass, 1)

    def test_hunger_mechanics(self):
        """Тест механики голода."""
        # Создаем существ
        herbivore = Herbivore(Coordinates(1, 1))
        predator = Predator(Coordinates(2, 2))
        initial_herb_hp = herbivore.hp
        initial_pred_hp = predator.hp
        
        # Размещаем на поле
        self.board.place_entity(herbivore.coordinates, herbivore)
        self.board.place_entity(predator.coordinates, predator)
        
        # Применяем урон от голода
        hunger_action = HungerAction(hunger_damage=SIMULATION_CONFIG['hunger_damage'])
        hunger_action.execute(self.board, self.simulation.logger)
        
        # Проверяем результат
        self.assertEqual(herbivore.hp, initial_herb_hp - SIMULATION_CONFIG['hunger_damage'])
        self.assertEqual(predator.hp, initial_pred_hp - SIMULATION_CONFIG['hunger_damage'])

    def test_health_check_mechanics(self):
        """Тест проверки здоровья и удаления мертвых существ."""
        # Создаем существо с минимальным здоровьем
        herbivore = Herbivore(Coordinates(1, 1))
        herbivore.hp = 1
        self.board.place_entity(herbivore.coordinates, herbivore)
        
        # Наносим урон
        herbivore.take_damage(1)
        
        # Проверяем здоровье
        health_check = HealthCheckAction()
        health_check.execute(self.board, self.simulation.logger)
        
        # Проверяем, что существо удалено
        self.assertIsNone(self.board.get_entity(herbivore.coordinates))

    def test_movement_and_interaction(self):
        """Тест движения и взаимодействия существ."""
        # Создаем травоядное и траву рядом
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(1, 2))
        
        self.board.place_entity(herbivore.coordinates, herbivore)
        self.board.place_entity(grass.coordinates, grass)
        
        # Выполняем ход
        move_action = MoveAction()
        move_action.execute(self.board, self.simulation.logger)
        
        # Проверяем, что трава съедена
        self.assertIsNone(self.board.get_entity(grass.coordinates))

    def _count_entities(self, entity_type) -> int:
        """Подсчет количества сущностей определенного типа."""
        return sum(1 for entity in self.board.entities.values() 
                  if isinstance(entity, entity_type))

    def test_full_simulation_cycle(self):
        """Тест полного цикла симуляции."""
        # Инициализация
        init_action = InitAction(herbivores=1, predators=1, grass=1)
        init_action.execute(self.board, self.simulation.logger)
        
        # Проверяем начальное состояние
        self.assertEqual(self._count_entities(Herbivore), 1)
        self.assertEqual(self._count_entities(Predator), 1)
        self.assertEqual(self._count_entities(Grass), 1)
        
        # Выполняем полный цикл действий
        actions = [
            SpawnGrassAction(min_grass=1, spawn_chance=1.0),
            MoveAction(),
            HungerAction(hunger_damage=1),
            HealthCheckAction()
        ]
        
        for action in actions:
            action.execute(self.board, self.simulation.logger)
        
        # Проверяем, что все действия выполнились без ошибок
        self.assertTrue(True)  # Если дошли до этой точки, значит ошибок не было

    def test_simulation_initialization(self):
        """Тест инициализации симуляции."""
        # Тест с параметрами по умолчанию
        default_sim = Simulation()
        self.assertEqual(default_sim.board.width, SIMULATION_CONFIG['board_size'])
        self.assertEqual(default_sim.board.height, SIMULATION_CONFIG['board_size'])
        self.assertIsNotNone(default_sim.logger)
        self.assertEqual(default_sim.turn_delay, SIMULATION_CONFIG['turn_delay'])
        self.assertFalse(default_sim.is_running)
        self.assertFalse(default_sim.is_paused)
        
        # Тест с кастомными параметрами
        custom_size = 10
        custom_sim = Simulation(board_size=custom_size)
        self.assertEqual(custom_sim.board.width, custom_size)
        self.assertEqual(custom_sim.board.height, custom_size)
        
        # Тест валидации параметров
        invalid_sizes = [0, -5]
        for invalid_size in invalid_sizes:
            with self.assertRaises(
                ValueError,
                msg=f"Должно вызывать ValueError для размера поля {invalid_size}"
            ):
                Simulation(board_size=invalid_size)

    def test_simulation_step(self):
        """Тест выполнения одного шага симуляции."""
        # Подготовка начального состояния
        init_action = InitAction(herbivores=2, predators=1, grass=3)
        init_action.execute(self.board, self.simulation.logger)
        
        # Добавляем действия в симуляцию
        self.simulation.turn_actions.extend([
            SpawnGrassAction(min_grass=1, spawn_chance=1.0),  # Гарантированный спавн травы
            MoveAction(),
            HungerAction(hunger_damage=1),
            HealthCheckAction()
        ])
        
        initial_state = {
            'herbivores': self._count_entities(Herbivore),
            'predators': self._count_entities(Predator),
            'grass': self._count_entities(Grass)
        }
        
        # Выполняем один шаг симуляции
        with patch('sys.stdout', new=StringIO()):  # Подавляем вывод
            self.simulation.next_turn()
        
        # Проверяем, что состояние изменилось
        final_state = {
            'herbivores': self._count_entities(Herbivore),
            'predators': self._count_entities(Predator),
            'grass': self._count_entities(Grass)
        }
        
        # Проверяем изменение счетчика ходов
        self.assertEqual(self.simulation.move_counter, 1)
        
        # Проверяем, что состояние изменилось хотя бы по одному параметру
        self.assertNotEqual(
            initial_state,
            final_state,
            "Шаг симуляции должен изменить состояние"
        )
        
        # Проверяем, что хотя бы одно из изменений произошло
        changes = [
            final_state['herbivores'] != initial_state['herbivores'],
            final_state['predators'] != initial_state['predators'],
            final_state['grass'] != initial_state['grass']
        ]
        self.assertTrue(
            any(changes),
            "Должно измениться количество хотя бы одного типа сущностей"
        )

    def test_simulation_run(self):
        """Тест запуска симуляции на несколько шагов."""
        # Подготовка начального состояния
        init_action = InitAction(herbivores=2, predators=1, grass=3)
        init_action.execute(self.board, self.simulation.logger)
        
        initial_state = {
            'herbivores': self._count_entities(Herbivore),
            'predators': self._count_entities(Predator),
            'grass': self._count_entities(Grass)
        }
        
        # Добавляем действия в симуляцию
        self.simulation.turn_actions.extend([
            SpawnGrassAction(min_grass=1, spawn_chance=1.0),
            MoveAction(),
            HungerAction(hunger_damage=1),
            HealthCheckAction()
        ])
        
        # Запускаем симуляцию на несколько шагов
        steps = 3
        with patch('sys.stdout', new=StringIO()), \
             patch('time.sleep'), \
             patch('keyboard.is_pressed', return_value=False):  # Симулируем отсутствие нажатий клавиш
            self.simulation.run(steps)
        
        # Проверяем финальное состояние
        final_state = {
            'herbivores': self._count_entities(Herbivore),
            'predators': self._count_entities(Predator),
            'grass': self._count_entities(Grass)
        }
        
        # Проверяем, что симуляция выполнилась и состояние изменилось
        self.assertNotEqual(
            initial_state, 
            final_state,
            f"Состояние должно измениться после {steps} шагов"
        )
        
        # Проверяем количество выполненных шагов
        self.assertEqual(self.simulation.move_counter, steps)
        
        # Проверяем остановку при нулевом количестве шагов
        with patch('sys.stdout', new=StringIO()):
            self.simulation.run(0)
            self.assertEqual(
                self.simulation.move_counter, 
                steps,
                "Счетчик ходов не должен измениться при steps=0"
            )


if __name__ == '__main__':
    unittest.main()
