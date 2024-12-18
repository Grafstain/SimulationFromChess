import unittest
from unittest.mock import Mock
from typing import List

from src.simulation_from_chess.actions.hunger_action import HungerAction
from src.simulation_from_chess.core.board import Board
from src.simulation_from_chess.core.coordinates import Coordinates
from src.simulation_from_chess.entities.grass import Grass
from src.simulation_from_chess.entities.herbivore import Herbivore
from src.simulation_from_chess.entities.predator import Predator
from src.simulation_from_chess.config import CREATURE_CONFIG

class TestHunger(unittest.TestCase):
    def setUp(self) -> None:
        """Создание тестового окружения."""
        self.board = Board(5, 5)
        self.hunger_action = HungerAction(hunger_damage=2)
        self.logger = Mock()

    def _setup_entities(self, entities: List[tuple]) -> None:
        """Размещение сущностей на доске."""
        for entity, coords in entities:
            self.board.place_entity(coords, entity)

    def test_hunger_damage(self) -> None:
        """Тест урона от голода для разных существ."""
        # Создаем существ
        herbivore = Herbivore(Coordinates(1, 1))
        predator = Predator(Coordinates(2, 2))
        grass = Grass(Coordinates(3, 3))  # Трава не должна получать урон
        
        initial_herbivore_hp = herbivore.hp
        initial_predator_hp = predator.hp
        
        self._setup_entities([
            (herbivore, herbivore.coordinates),
            (predator, predator.coordinates),
            (grass, grass.coordinates)
        ])
        
        # Применяем урон от голода
        self.hunger_action.execute(self.board, self.logger)
        
        # Проверяем урон для травоядного
        self.assertEqual(
            herbivore.hp,
            initial_herbivore_hp - self.hunger_action.hunger_damage,
            "Неверный урон от голода для травоядного"
        )
        
        # Проверяем урон для хищника
        self.assertEqual(
            predator.hp,
            initial_predator_hp - self.hunger_action.hunger_damage,
            "Неверный урон от голода для хищника"
        )
        
        # Проверяем, что трава не получила урон
        self.assertIsNotNone(
            self.board.get_entity(grass.coordinates),
            "Трава не должна получать урон от голода"
        )

    def test_death_from_hunger(self) -> None:
        """Тест смерти существа от голода."""
        herbivore = Herbivore(Coordinates(1, 1))
        # Оставляем HP меньше урона от голода
        herbivore.hp = self.hunger_action.hunger_damage - 1
        
        self._setup_entities([(herbivore, herbivore.coordinates)])
        
        # Применяем урон от голода
        self.hunger_action.execute(self.board, self.logger)
        
        # Проверяем, что существо умерло
        self.assertLessEqual(herbivore.hp, 0, "Существо должно умереть от голода")
        
        # Проверяем, что существо все еще на доске для логирования
        self.assertIsNotNone(
            self.board.get_entity(herbivore.coordinates),
            "Мертвое существо должно оставаться на доске один ход для логирования"
        )
        
        # Проверяем, что существо добавлено в список мертвых
        self.assertIn(
            herbivore.coordinates,
            self.hunger_action.dead_entities,
            "Мертвое существо должно быть добавлено в список для удаления"
        )
        
        # Выполняем следующий ход
        self.hunger_action.execute(self.board, self.logger)
        
        # Теперь проверяем, что существо удалено с доски
        self.assertIsNone(
            self.board.get_entity(herbivore.coordinates),
            "Мертвое существо должно быть удалено с доски на следующий ход"
        )

    def test_hunger_recovery(self) -> None:
        """Тест восстановления HP при питании."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(1, 2))
        
        # Наносим урон травоядному
        initial_damage = 10
        herbivore.take_damage(initial_damage)
        initial_hp = herbivore.hp
        
        self._setup_entities([
            (herbivore, herbivore.coordinates),
            (grass, grass.coordinates)
        ])
        
        # Травоядное ест траву
        success, _ = herbivore.interact_with_target(self.board, grass)
        
        self.assertTrue(success, "Питание должно быть успешным")
        self.assertGreater(
            herbivore.hp,
            initial_hp,
            "HP должно увеличиться после питания"
        )
        self.assertLessEqual(
            herbivore.hp,
            CREATURE_CONFIG['herbivore']['initial_hp'],
            "HP не должно превышать максимальное значение"
        )

    def test_hunger_logging(self) -> None:
        """Тест логирования урона от голода."""
        herbivore = Herbivore(Coordinates(1, 1))
        # Устанавливаем HP так, чтобы существо умерло от голода
        herbivore.hp = self.hunger_action.hunger_damage - 1
        self._setup_entities([(herbivore, herbivore.coordinates)])
        
        # Применяем урон от голода
        self.hunger_action.execute(self.board, self.logger)
        
        # Проверяем логирование смерти
        self.logger.log_action.assert_called_with(
            herbivore,
            "Погиб",
            f"от голода на координатах ({herbivore.coordinates.x}, {herbivore.coordinates.y})"
        )