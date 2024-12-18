from unittest import TestCase
from src.simulation_from_chess.utils.logger import Logger
from src.simulation_from_chess.entities.herbivore import Herbivore
from src.simulation_from_chess.entities.predator import Predator
from src.simulation_from_chess.core.coordinates import Coordinates
from src.simulation_from_chess.entities.grass import Grass

class TestLogger(TestCase):
    def setUp(self):
        self.logger = Logger()
        self.herbivore = Herbivore(Coordinates(1, 1))
        self.predator = Predator(Coordinates(2, 2))

    def test_log_action_for_creature(self):
        """Тест логирования действий существа."""
        self.logger.log_action(self.herbivore, "Планирует движение", "к Grass на (2, 2)")
        
        # Проверяем, что действие сохранено в состоянии существа
        entity_key = str(self.herbivore)
        self.assertIn(entity_key, self.logger.creatures_state)
        self.assertEqual(
            self.logger.creatures_state[entity_key]['action'],
            "Планирует движение к Grass на (2, 2)"
        )

    def test_log_system_message(self):
        """Тест логирования системного сообщения."""
        self.logger.log_action(None, "Система", "тестовое сообщение")
        self.assertEqual(len(self.logger.system_logs), 1)
        self.assertEqual(
            self.logger.system_logs[0],
            "Система: тестовое сообщение"
        )

    def test_clear_logs(self):
        """Тест очистки логов."""
        # Добавляем действие и системное сообщение
        self.logger.log_action(self.herbivore, "Действие", "детали")
        self.logger.log_action(None, "Система", "сообщение")
        
        # Очищаем логи
        self.logger.clear_logs()
        
        # Проверяем, что системные сообщения очищены
        self.assertEqual(len(self.logger.system_logs), 0)
        
        # Проверяем, что действия существ очищены, но информация о существах сохранена
        entity_key = str(self.herbivore)
        self.assertIn(entity_key, self.logger.creatures_state)
        self.assertEqual(self.logger.creatures_state[entity_key]['action'], '')

    def test_log_creatures_state(self):
        """Тест обновления состояния существ."""
        entities = {
            self.herbivore.coordinates: self.herbivore,
            self.predator.coordinates: self.predator
        }
        
        self.logger.log_creatures_state(entities)
        
        # Проверяем, что состояния обоих существ сохранены
        self.assertEqual(len(self.logger.creatures_state), 2)
        self.assertIn(str(self.herbivore), self.logger.creatures_state)
        self.assertIn(str(self.predator), self.logger.creatures_state)

    def test_log_initial_creatures_state(self):
        """Тест логирования начального состояния размещенных существ."""
        # Создаем несколько существ с разными координатами
        herbivore1 = Herbivore(Coordinates(1, 1))
        herbivore2 = Herbivore(Coordinates(2, 2))
        predator1 = Predator(Coordinates(3, 3))
        grass = Grass(Coordinates(4, 4))  # Трава не должна попасть в лог существ
        
        # Создаем словарь сущностей, имитируя доску
        entities = {
            herbivore1.coordinates: herbivore1,
            herbivore2.coordinates: herbivore2,
            predator1.coordinates: predator1,
            grass.coordinates: grass
        }
        
        # Логируем состояние
        self.logger.log_creatures_state(entities)
        
        # Проверяем количество существ в логе (должно быть 3, без травы)
        self.assertEqual(len(self.logger.creatures_state), 3)
        
        # Проверяем наличие всех существ в логе
        self.assertIn(str(herbivore1), self.logger.creatures_state)
        self.assertIn(str(herbivore2), self.logger.creatures_state)
        self.assertIn(str(predator1), self.logger.creatures_state)
        
        # Проверяем корректность сохраненной информации для каждого существа
        for entity in [herbivore1, herbivore2, predator1]:
            state = self.logger.creatures_state[str(entity)]
            self.assertEqual(state['type'], entity.__class__.__name__)
            self.assertEqual(state['hp'], entity.hp)
            self.assertEqual(state['coordinates'], entity.coordinates)
            self.assertEqual(state['action'], '')  # Начальное действие должно быть пустым

        # Проверяем, что трава не попала в лог существ
        self.assertNotIn(str(grass), self.logger.creatures_state)

    def test_log_creatures_state_updates(self):
        """Тест обновления состояния существ при изменении их параметров."""
        # Создаем существо и добавляем его в начальное состояние
        herbivore = Herbivore(Coordinates(1, 1))
        entities = {herbivore.coordinates: herbivore}
        self.logger.log_creatures_state(entities)
        
        # Проверяем начальное состояние
        initial_state = self.logger.creatures_state[str(herbivore)]
        self.assertEqual(initial_state['coordinates'], Coordinates(1, 1))
        self.assertEqual(initial_state['hp'], herbivore.hp)
        self.assertEqual(initial_state['action'], '')
        
        # Добавляем действие и проверяем его сохранение
        self.logger.log_action(herbivore, "Планирует движение", "к Grass на (2, 2)")
        self.logger.log_creatures_state(entities)
        self.assertEqual(
            self.logger.creatures_state[str(herbivore)]['action'],
            "Планирует движение к Grass на (2, 2)"
        )