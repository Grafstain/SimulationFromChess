import unittest
from typing import List
from unittest.mock import Mock

from src.simulation_from_chess.core.board import Board
from src.simulation_from_chess.core.coordinates import Coordinates
from src.simulation_from_chess.entities.grass import Grass
from src.simulation_from_chess.entities.herbivore import Herbivore
from src.simulation_from_chess.entities.predator import Predator
from src.simulation_from_chess.actions.hunger_action import HungerAction
from src.simulation_from_chess.config import CREATURE_CONFIG


class TestHunger(unittest.TestCase):
    def setUp(self) -> None:
        """Создание тестового окружения."""
        self.board = Board(5, 5)
        self.hunger_action = HungerAction(hunger_damage=2)
        # Создаем мок-логгер
        self.logger = Mock()
        self.logger.log_action = Mock()

    def _setup_entities(self, entities: List[tuple]) -> None:
        """
        Вспомогательный метод для размещения сущностей на доске.
        
        Args:
            entities: Список кортежей (сущность, координаты)
        """
        for entity, coords in entities:
            self.board.place_entity(coords, entity)

    def test_basic_hunger_damage(self) -> None:
        """Тест базового урона от голода."""
        herbivore = Herbivore(Coordinates(1, 1))
        initial_hp = herbivore.hp
        
        self._setup_entities([(herbivore, herbivore.coordinates)])
        
        self.hunger_action.execute(self.board, self.logger)
        
        self.assertEqual(
            herbivore.hp, 
            initial_hp - self.hunger_action.hunger_damage,
            f"HP травоядного должно уменьшиться на {self.hunger_action.hunger_damage}"
        )

    def test_multiple_creatures_hunger(self) -> None:
        """Тест урона от голода для нескольких существ."""
        herbivore = Herbivore(Coordinates(1, 1))
        predator = Predator(Coordinates(2, 2))
        
        self._setup_entities([
            (herbivore, herbivore.coordinates),
            (predator, predator.coordinates)
        ])
        
        initial_herbivore_hp = herbivore.hp
        initial_predator_hp = predator.hp
        
        self.hunger_action.execute(self.board, self.logger)
        
        # Проверяем урон от голода для травоядного
        self.assertEqual(
            herbivore.hp,
            initial_herbivore_hp - self.hunger_action.hunger_damage,
            "Неверный урон от голода для травоядного"
        )
        
        # Проверяем урон от голода для хищника
        self.assertEqual(
            predator.hp,
            initial_predator_hp - self.hunger_action.hunger_damage,
            "Неверный урон от голода для хищника"
        )

    def test_eating_mechanics(self) -> None:
        """Тест механики питания травоядного."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(1, 2))
        
        # Наносим урон травоядному
        damage = 5
        herbivore.take_damage(damage)
        initial_hp = herbivore.hp
        
        self._setup_entities([
            (herbivore, herbivore.coordinates),
            (grass, grass.coordinates)
        ])
        
        # Проверяем взаимодействие с травой
        success, _ = herbivore.interact_with_target(self.board, grass)
        
        self.assertTrue(success, "Взаимодействие с травой должно быть успешным")
        self.assertIsNone(
            self.board.get_entity(grass.coordinates),
            "Трава должна быть съедена"
        )
        
        # Проверяем восстановление HP
        expected_hp = min(
            CREATURE_CONFIG['herbivore']['initial_hp'],
            initial_hp + CREATURE_CONFIG['herbivore']['food_value']
        )
        self.assertEqual(
            herbivore.hp,
            expected_hp,
            f"HP травоядного должно восстановиться до {expected_hp}"
        )

    def test_predator_eating_mechanics(self) -> None:
        """Тест механики питания хищника."""
        predator = Predator(Coordinates(1, 1))
        herbivore = Herbivore(Coordinates(1, 2))
        
        # Наносим урон хищнику
        damage = 5
        predator.take_damage(damage)
        initial_predator_hp = predator.hp
        initial_herbivore_hp = herbivore.hp
        
        self._setup_entities([
            (predator, predator.coordinates),
            (herbivore, herbivore.coordinates)
        ])
        
        # Устанавливаем гарантированный успех атаки
        predator.set_hunt_result(True)
        
        # Проверяем атаку хищника
        success, _ = predator.interact_with_target(self.board, herbivore)
        
        self.assertTrue(success, "Атака хищника должна быть успешной")
        self.assertEqual(
            herbivore.hp,
            initial_herbivore_hp - CREATURE_CONFIG['predator']['attack_damage'],
            "Неверный урон от атаки хищника"
        )
        
        # Если травоядное погибло, проверяем восстановление HP хищника
        if herbivore.hp <= 0:
            expected_hp = min(
                CREATURE_CONFIG['predator']['initial_hp'],
                initial_predator_hp + CREATURE_CONFIG['predator']['food_value']
            )
            self.assertEqual(
                predator.hp,
                expected_hp,
                f"HP хищника должно восстановиться до {expected_hp}"
            )
            self.assertIsNone(
                self.board.get_entity(herbivore.coordinates),
                "Мертвое травоядное должно быть удалено с поля"
            )

    def test_max_hp_limit(self) -> None:
        """Тест ограничения максимального HP при питании."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(1, 2))
        
        self._setup_entities([
            (herbivore, herbivore.coordinates),
            (grass, grass.coordinates)
        ])
        
        # Проверяем, что HP не превышает максимальное значение
        herbivore.interact_with_target(self.board, grass)
        self.assertLessEqual(
            herbivore.hp,
            CREATURE_CONFIG['herbivore']['initial_hp'],
            "HP не должно превышать максимальное значение"
        )

    def test_successful_hunt(self) -> None:
        """Тест успешной охоты хищника."""
        predator = Predator(Coordinates(1, 1))
        herbivore = Herbivore(Coordinates(1, 2))
        initial_herbivore_hp = herbivore.hp
        
        # Устанавливаем гарантированный успех охоты
        predator.set_hunt_result(True)
        
        self._setup_entities([
            (predator, predator.coordinates),
            (herbivore, herbivore.coordinates)
        ])
        
        success, message = predator.interact_with_target(self.board, herbivore)
        
        self.assertTrue(success, "Охота должна быть успешной")
        self.assertEqual(
            herbivore.hp,
            initial_herbivore_hp - CREATURE_CONFIG['predator']['attack_damage'],
            "Неверный урон от атаки хищника"
        )
        self.assertIn("Успешная атака", message, "Неверное сообщение об успешной атаке")

    def test_failed_hunt(self) -> None:
        """Тест неудачной охоты хищника."""
        predator = Predator(Coordinates(1, 1))
        herbivore = Herbivore(Coordinates(1, 2))
        initial_herbivore_hp = herbivore.hp
        
        # Устанавливаем гарантированный провал охоты
        predator.set_hunt_result(False)
        
        self._setup_entities([
            (predator, predator.coordinates),
            (herbivore, herbivore.coordinates)
        ])
        
        success, message = predator.interact_with_target(self.board, herbivore)
        
        self.assertFalse(success, "Охота должна быть неудачной")
        self.assertEqual(
            herbivore.hp,
            initial_herbivore_hp,
            "HP травоядного не должно измениться при неудачной охоте"
        )
        self.assertIn("избежало атаки", message, "Неверное сообщение о неудачной атаке")

    def test_hunt_with_random_chance(self) -> None:
        """Тест случайности успеха охоты."""
        predator = Predator(Coordinates(1, 1))
        herbivore = Herbivore(Coordinates(1, 2))
        
        # Не устанавливаем принудительный результат
        successes = []
        for _ in range(100):  # Достаточно большое количество попыток
            success = predator.try_attack_herbivore(herbivore)
            successes.append(success)
        
        # Проверяем, что есть как успешные, так и неудачные попытки
        self.assertTrue(
            any(successes) and not all(successes),
            "Охота должна быть как успешной, так и неудачной при случайных попытках"
        )
        
        # Проверяем, что процент успешных охот примерно соответствует ожидаемому
        success_rate = sum(successes) / len(successes)
        expected_rate = 1 - CREATURE_CONFIG['predator']['escape_chance']
        self.assertAlmostEqual(
            success_rate,
            expected_rate,
            delta=0.2,  # Допускаем отклонение в 20%
            msg="Процент успешных охот значительно отличается от ожидаемого"
        )