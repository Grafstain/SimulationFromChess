import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

from src.simulation_from_chess.utils.Logger import Logger
from src.simulation_from_chess.entities.herbivore import Herbivore
from src.simulation_from_chess.entities.predator import Predator
from src.simulation_from_chess.core.coordinates import Coordinates

class TestLogger(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения."""
        self.logger = Logger()
        self.test_entity = Herbivore(Coordinates(1, 1))
        self.test_action = "Тест"
        self.test_description = "Описание"
        
    def _add_test_action(self):
        """Вспомогательный метод для добавления тестового действия."""
        self.logger.log_action(self.test_entity, self.test_action, self.test_description)

    def test_logger_initialization(self):
        """Тест инициализации логгера."""
        self.assertIsNotNone(self.logger.actions_log)
        self.assertEqual(len(self.logger.actions_log), 0, "Лог действий должен быть пустым при инициализации")

    def test_log_action_basic(self):
        """Тест базового логирования действий."""
        self._add_test_action()
        self.assertTrue(len(self.logger.actions_log) > 0, "Действие не было добавлено в лог")

    def test_log_creatures_state(self):
        """Тест логирования состояния существ."""
        test_entities = {
            "1_1": self.test_entity,
            "2_2": Predator(Coordinates(2, 2))
        }
        
        try:
            self.logger.log_creatures_state(test_entities)
            success = True
        except Exception as e:
            success = False
            self.fail(f"log_creatures_state вызвал неожиданную ошибку: {str(e)}")
        
        self.assertTrue(success, "log_creatures_state должен выполняться без ошибок")

    def test_clear_actions_log(self):
        """Тест очистки лога действий."""
        # Добавляем несколько действий
        self._add_test_action()
        self._add_test_action()
        
        self.assertTrue(len(self.logger.actions_log) > 0, "Действия не были добавлены в лог")
        
        # Очищаем лог
        self.logger.actions_log.clear()
        self.assertEqual(len(self.logger.actions_log), 0, "Лог не был очищен")

    def test_log_invalid_actions(self):
        """Тест логирования с некорректными данными."""
        test_cases = [
            (None, "", ""),           # Пустые строки
            (None, None, None),       # None значения
            (123, 456, 789),          # Некорректные типы данных
            ("", None, 123),          # Смешанные некорректные данные
            (self.test_entity, "", None)  # Частично корректные данные
        ]
        
        for entity, action_type, description in test_cases:
            try:
                self.logger.log_action(entity, action_type, description)
                success = True
            except Exception as e:
                self.fail(f"Логирование вызвало неожиданную ошибку для данных: "
                         f"({entity}, {action_type}, {description}). Ошибка: {str(e)}")

    def test_log_multiple_actions(self):
        """Тест логирования нескольких действий."""
        test_actions = [
            (Herbivore(Coordinates(1, 1)), "Действие1", "Описание1"),
            (Predator(Coordinates(2, 2)), "Действие2", "Описание2"),
            (None, "Действие3", "Описание3")
        ]
        
        initial_log_size = len(self.logger.actions_log)
        
        for entity, action_type, description in test_actions:
            self.logger.log_action(entity, action_type, description)
        
        final_log_size = len(self.logger.actions_log)
        self.assertGreater(
            final_log_size, 
            initial_log_size, 
            "Размер лога должен увеличиться после добавления действий"
        )

if __name__ == '__main__':
    unittest.main()