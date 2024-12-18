import unittest
from src.simulation_from_chess.core.board import Board
from src.simulation_from_chess.core.coordinates import Coordinates
from src.simulation_from_chess.core.game_state import GameState, EntityState
from src.simulation_from_chess.entities.herbivore import Herbivore
from src.simulation_from_chess.entities.predator import Predator
from src.simulation_from_chess.entities.grass import Grass

class TestGameState(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения."""
        self.board = Board(5, 5)
        self.game_state = GameState()

    def test_save_and_get_entity_state(self):
        """Тест сохранения и получения состояния сущности."""
        # Создаем тестовое состояние
        entity_id = 1
        turn = 0
        state = EntityState(
            coordinates=Coordinates(1, 1),
            hp=100,
            planned_action=("Движение", Coordinates(2, 2)),
            performed_action=("Переместился", Coordinates(2, 2))
        )
        
        # Сохраняем состояние
        self.game_state.save_entity_state(turn, entity_id, state)
        
        # Получаем состояние
        retrieved_state = self.game_state.get_entity_state(turn, entity_id)
        
        # Проверяем соответствие
        self.assertEqual(retrieved_state.coordinates, state.coordinates)
        self.assertEqual(retrieved_state.hp, state.hp)
        self.assertEqual(retrieved_state.planned_action, state.planned_action)
        self.assertEqual(retrieved_state.performed_action, state.performed_action)

    def test_nonexistent_state(self):
        """Тест получения несуществующего состояния."""
        state = self.game_state.get_entity_state(0, 999)
        self.assertIsNone(state)

    def test_state_history(self):
        """Тест истории состояний сущности."""
        entity_id = 1
        
        # Создаем несколько состояний
        states = [
            EntityState(coordinates=Coordinates(1, 1), hp=100),
            EntityState(coordinates=Coordinates(1, 2), hp=90),
            EntityState(coordinates=Coordinates(2, 2), hp=80)
        ]
        
        # Сохраняем состояния
        for turn, state in enumerate(states):
            self.game_state.save_entity_state(turn, entity_id, state)
        
        # Проверяем историю
        for turn, expected_state in enumerate(states):
            actual_state = self.game_state.get_entity_state(turn, entity_id)
            self.assertEqual(actual_state.coordinates, expected_state.coordinates)
            self.assertEqual(actual_state.hp, expected_state.hp)

    def test_clear_old_states(self):
        """Тест очистки старых состояний."""
        entity_id = 1
        total_turns = 5
        keep_turns = 2
        
        # Создаем состояния для нескольких ходов
        for turn in range(total_turns):
            state = EntityState(
                coordinates=Coordinates(1, turn + 1),
                hp=100 - turn * 10
            )
            self.game_state.save_entity_state(turn, entity_id, state)
        
        # Очищаем старые состояния
        self.game_state.clear_old_states(keep_turns=keep_turns)
        
        # Проверяем удаление старых состояний
        for turn in range(total_turns - keep_turns):
            self.assertIsNone(
                self.game_state.get_entity_state(turn, entity_id),
                f"Состояние для хода {turn} должно быть удалено"
            )
        
        # Проверяем сохранение последних состояний
        for turn in range(total_turns - keep_turns, total_turns):
            self.assertIsNotNone(
                self.game_state.get_entity_state(turn, entity_id),
                f"Состояние для хода {turn} должно быть сохранено"
            )

    def test_multiple_entities_state(self):
        """Тест состояний нескольких сущностей."""
        # Создаем сущности
        entities = {
            1: Herbivore(Coordinates(1, 1)),
            2: Predator(Coordinates(2, 2)),
            3: Grass(Coordinates(3, 3))
        }
        
        # Сохраняем начальные состояния
        for entity_id, entity in entities.items():
            state = EntityState(
                coordinates=entity.coordinates,
                hp=getattr(entity, 'hp', None)
            )
            self.game_state.save_entity_state(0, entity_id, state)
        
        # Проверяем состояния
        for entity_id, entity in entities.items():
            state = self.game_state.get_entity_state(0, entity_id)
            self.assertEqual(state.coordinates, entity.coordinates)
            if hasattr(entity, 'hp'):
                self.assertEqual(state.hp, entity.hp)

    def test_state_updates(self):
        """Тест обновления состояний."""
        entity_id = 1
        turn = 0
        
        # Создаем начальное состояние
        initial_state = EntityState(
            coordinates=Coordinates(1, 1),
            hp=100
        )
        self.game_state.save_entity_state(turn, entity_id, initial_state)
        
        # Обновляем состояние
        updated_state = EntityState(
            coordinates=Coordinates(2, 2),
            hp=90,
            performed_action=("Переместился", Coordinates(2, 2))
        )
        self.game_state.save_entity_state(turn, entity_id, updated_state)
        
        # Проверяем обновление
        current_state = self.game_state.get_entity_state(turn, entity_id)
        self.assertEqual(current_state.coordinates, updated_state.coordinates)
        self.assertEqual(current_state.hp, updated_state.hp)
        self.assertEqual(current_state.performed_action, updated_state.performed_action) 