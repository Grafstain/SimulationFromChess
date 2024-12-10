import unittest
from src.simulation_from_chess.utils.logger import Logger
from src.simulation_from_chess.entities.herbivore import Herbivore
from src.simulation_from_chess.entities.predator import Predator
from src.simulation_from_chess.core.coordinates import Coordinates

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.herbivore = Herbivore(Coordinates(1, 1))
        self.predator = Predator(Coordinates(2, 2))

    def test_basic_action_logging(self):
        """Тест базового логирования действий."""
        self.logger.log_action(self.herbivore, "Переместился", "на координаты (2, 2)")
        
        self.assertIn(self.herbivore, self.logger.actions_log)
        self.assertEqual(
            self.logger.actions_log[self.herbivore],
            "Переместился на координаты (2, 2)"
        )

    def test_death_logging_by_predator(self):
        """Тест логирования смерти от хищника."""
        self.logger.log_action(self.herbivore, "Погиб", killer=self.predator)
        
        self.assertIn(self.herbivore, self.logger.dead_entities)
        coords, death_text = self.logger.dead_entities[self.herbivore]
        self.assertEqual(death_text, f"Был съеден существом {self.predator}")

    def test_death_logging_by_hunger(self):
        """Тест логирования смерти от голода."""
        death_details = "от голода на координатах (1, 1)"
        self.logger.log_action(self.herbivore, "Погиб", death_details)
        
        self.assertIn(self.herbivore, self.logger.dead_entities)
        coords, death_text = self.logger.dead_entities[self.herbivore]
        self.assertEqual(death_text, f"Погиб {death_details}")

    def test_dead_entities_clearing(self):
        """Тест очистки списка мертвых существ после вывода."""
        self.logger.log_action(self.herbivore, "Погиб", killer=self.predator)
        self.assertIn(self.herbivore, self.logger.dead_entities)
        
        # Вызываем вывод состояния
        self.logger.log_creatures_state({})
        
        # Проверяем, что список мертвых существ очищен
        self.assertEqual(len(self.logger.dead_entities), 0)

    def test_multiple_actions_same_creature(self):
        """Тест обновления действий для одного существа."""
        self.logger.log_action(self.herbivore, "Действие1", "детали1")
        self.logger.log_action(self.herbivore, "Действие2", "детали2")
        
        # Должно сохраниться только последнее действие
        self.assertEqual(
            self.logger.actions_log[self.herbivore],
            "Действие2 детали2"
        )

    def test_complex_move_result_logging(self):
        """Тест логирования сложного результата перемещения."""
        # Симулируем результат успешной охоты
        move_result = [
            ("Успешная охота", "здоровье восстановлено на 30"),
            ("Погиб", "", self.herbivore, self.predator)
        ]
        
        # Логируем каждое действие из результата
        for action in move_result:
            if len(action) == 4:  # Действие с информацией о смерти
                action_type, details, target, killer = action
                self.logger.log_action(target, action_type, details, killer=killer)
            else:  # Обычное действие
                self.logger.log_action(self.predator, action[0], action[1])
        
        # Проверяем логирование действия хищника
        self.assertIn(self.predator, self.logger.actions_log)
        self.assertTrue(
            self.logger.actions_log[self.predator].startswith("Успешная охота")
        )
        
        # Проверяем логирование смерти травоядного
        self.assertIn(self.herbivore, self.logger.dead_entities)
        _, death_text = self.logger.dead_entities[self.herbivore]
        self.assertTrue(death_text.startswith("Был съеден существом"))

if __name__ == '__main__':
    unittest.main()